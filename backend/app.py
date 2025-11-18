"""
PhD Application Automator - Main Flask Application
A comprehensive system for discovering and applying to PhD programs worldwide
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from models import init_db, close_session
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_class = get_config()
app.config.from_object(config_class)

# Initialize extensions
CORS(app, origins=app.config['CORS_ORIGINS'])
jwt = JWTManager(app)

# Initialize database
database_url = app.config['SQLALCHEMY_DATABASE_URI']
init_db(database_url, echo=app.config['DEBUG'])

# Setup logging
def setup_logging():
    """Configure application logging"""
    if not app.debug:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # File handler for error logs
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)

    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.info('PhD Application Automator startup')

setup_logging()


# Request hooks
@app.before_request
def before_request():
    """Log request details"""
    if app.debug:
        app.logger.debug(f'{request.method} {request.path} from {request.remote_addr}')


@app.after_request
def after_request(response):
    """Add headers and log response"""
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    if app.debug:
        app.logger.debug(f'Response: {response.status_code}')

    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close database session after request"""
    close_session()


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'error': 'Bad Request',
        'message': str(error)
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 errors"""
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return jsonify({
        'error': 'Forbidden',
        'message': 'You do not have permission to access this resource'
    }), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f'Internal error: {str(error)}')
    close_session()  # Rollback database session
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired tokens"""
    return jsonify({
        'error': 'Token Expired',
        'message': 'The authentication token has expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid tokens"""
    return jsonify({
        'error': 'Invalid Token',
        'message': 'The authentication token is invalid'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing tokens"""
    return jsonify({
        'error': 'No Token',
        'message': 'Authentication token is missing'
    }), 401


# Import and register blueprints (routes)
from routes.auth import auth_bp
from routes.universities import universities_bp
from routes.professors import professors_bp
from routes.applications import applications_bp
from routes.emails import emails_bp
from routes.analytics import analytics_bp
from routes.user import user_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(universities_bp, url_prefix='/api/universities')
app.register_blueprint(professors_bp, url_prefix='/api/professors')
app.register_blueprint(applications_bp, url_prefix='/api/applications')
app.register_blueprint(emails_bp, url_prefix='/api/emails')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(user_bp, url_prefix='/api/user')


# Root endpoints
@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'PhD Application Automator API',
        'version': '1.0.0',
        'description': 'AI-powered PhD application discovery and automation system',
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'auth': '/api/auth',
            'universities': '/api/universities',
            'professors': '/api/professors',
            'applications': '/api/applications',
            'emails': '/api/emails',
            'analytics': '/api/analytics',
            'user': '/api/user',
        },
        'documentation': '/api/docs'
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected',
        'environment': app.config['ENVIRONMENT']
    })


@app.route('/api/docs')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        'name': 'PhD Application Automator API Documentation',
        'version': '1.0.0',
        'base_url': request.url_root + 'api',
        'authentication': 'JWT Bearer Token',
        'endpoints': {
            'auth': {
                'POST /auth/register': 'Register new user',
                'POST /auth/login': 'Login and get JWT token',
                'POST /auth/logout': 'Logout user',
                'POST /auth/refresh': 'Refresh JWT token',
                'POST /auth/forgot-password': 'Request password reset',
                'POST /auth/reset-password': 'Reset password',
            },
            'universities': {
                'GET /universities/search': 'Search universities with filters',
                'GET /universities/:id': 'Get university details',
                'POST /universities/discover': 'Trigger university discovery (scraping)',
                'GET /universities/:id/professors': 'Get professors at university',
                'GET /universities/favorites': 'Get favorited universities',
                'POST /universities/:id/favorite': 'Toggle favorite status',
            },
            'professors': {
                'GET /professors/search': 'Search professors with filters',
                'GET /professors/:id': 'Get professor details',
                'POST /professors/discover': 'Trigger professor discovery',
                'GET /professors/:id/publications': 'Get professor publications',
                'PUT /professors/:id/notes': 'Update professor notes',
            },
            'emails': {
                'POST /emails/generate': 'Generate batch of personalized emails',
                'GET /emails/drafts': 'Get draft emails',
                'GET /emails/:id': 'Get email details',
                'PUT /emails/:id': 'Update email',
                'DELETE /emails/:id': 'Delete email draft',
                'POST /emails/batch/approve': 'Approve batch of emails',
                'POST /emails/batch/send': 'Send approved batch',
                'GET /emails/history': 'Get email history',
                'GET /emails/:id/status': 'Get email sending status',
            },
            'applications': {
                'GET /applications': 'Get all applications',
                'GET /applications/:id': 'Get application details',
                'POST /applications': 'Create new application',
                'PUT /applications/:id': 'Update application',
                'PUT /applications/:id/status': 'Update application status',
                'POST /applications/:id/note': 'Add note to application',
                'GET /applications/stats': 'Get application statistics',
            },
            'analytics': {
                'GET /analytics/dashboard': 'Get dashboard statistics',
                'GET /analytics/response-rate': 'Get email response rates',
                'GET /analytics/by-country': 'Get applications by country',
                'GET /analytics/success-funnel': 'Get application funnel data',
                'GET /analytics/export': 'Export analytics report',
            },
            'user': {
                'GET /user/profile': 'Get user profile',
                'PUT /user/profile': 'Update user profile',
                'POST /user/cv-upload': 'Upload CV',
                'GET /user/preferences': 'Get user preferences',
                'PUT /user/preferences': 'Update preferences',
            }
        }
    })


if __name__ == '__main__':
    """Run the application"""
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🎓 PhD APPLICATION AUTOMATOR API                        ║
    ║                                                              ║
    ║     AI-Powered Global PhD Opportunity Discovery             ║
    ║                                                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║     🌐 Server running on http://localhost:{:<5}             ║
    ║     📚 API Documentation: http://localhost:{}/api/docs     ║
    ║     ❤️  Health Check: http://localhost:{}/api/health       ║
    ║                                                              ║
    ║     Environment: {:<40}    ║
    ║     Debug Mode: {:<41}    ║
    ║     Database: {:<42}    ║
    ║                                                              ║
    ║     Press CTRL+C to stop the server                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """.format(
        port, port, port,
        app.config['ENVIRONMENT'],
        str(debug),
        app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1]
    ))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )
