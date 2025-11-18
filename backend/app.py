"""
Main Flask application entry point
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import get_config
from models import db, init_db

# Import routes (will be created later)
# from routes import auth, universities, professors, applications, emails, analytics, user, system

# Create Flask application
def create_app(config_name=None):
    """Application factory pattern"""

    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    config.init_app(app)

    # Initialize extensions
    init_extensions(app)

    # Register blueprints (routes)
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


def init_extensions(app):
    """Initialize Flask extensions"""

    # Database
    init_db(app)

    # Database migrations
    migrate = Migrate(app, db)

    # CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # JWT
    jwt = JWTManager(app)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'error': 'Token has expired',
            'message': 'The token has expired. Please login again.'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'error': 'Invalid token',
            'message': 'Token validation failed. Please login again.'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'success': False,
            'error': 'Authorization required',
            'message': 'No authorization token provided.'
        }), 401


def register_blueprints(app):
    """Register API blueprints"""

    # Import routes
    from routes.auth import auth_bp
    # TODO: Uncomment when routes are created
    # from routes.universities import universities_bp
    # from routes.professors import professors_bp
    # from routes.applications import applications_bp
    # from routes.emails import emails_bp
    # from routes.analytics import analytics_bp
    # from routes.user import user_bp
    # from routes.system import system_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(universities_bp, url_prefix='/api/universities')
    # app.register_blueprint(professors_bp, url_prefix='/api/professors')
    # app.register_blueprint(applications_bp, url_prefix='/api/applications')
    # app.register_blueprint(emails_bp, url_prefix='/api/emails')
    # app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    # app.register_blueprint(user_bp, url_prefix='/api/user')
    # app.register_blueprint(system_bp, url_prefix='/api/system')

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'success': True,
            'message': 'PhD Application Automator API is running',
            'version': '1.0.0'
        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint"""
        return jsonify({
            'success': True,
            'message': 'PhD Application Automator API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'universities': '/api/universities',
                'professors': '/api/professors',
                'applications': '/api/applications',
                'emails': '/api/emails',
                'analytics': '/api/analytics',
                'user': '/api/user',
                'system': '/api/system',
                'health': '/api/health'
            }
        }), 200


def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for this endpoint'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred'
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle any uncaught exceptions"""
        app.logger.error(f"Unhandled exception: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print("=" * 60)
    print("🚀 PhD Application Automator API")
    print("=" * 60)
    print(f"📡 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
