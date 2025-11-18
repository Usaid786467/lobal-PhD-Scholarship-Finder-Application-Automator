"""
Main Flask Application
PhD Application Automator Backend Server
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import get_config
from models import db
from services.utils.logger import setup_logging


def create_app(config_name=None):
    """Application factory pattern"""

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    config.init_app(app)

    # Setup logging
    setup_logging(app)
    app.logger.info('Starting PhD Application Automator...')

    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # Register blueprints (routes)
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # JWT callbacks
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'error': 'Token has expired',
            'message': 'Please log in again'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'error': 'Invalid token',
            'message': 'Please log in again'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({
            'success': False,
            'error': 'Missing authorization',
            'message': 'Please provide a valid token'
        }), 401

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'success': True,
            'message': 'PhD Application Automator is running',
            'version': '1.0.0'
        })

    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'success': True,
            'message': 'PhD Application Automator API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth/*',
                'universities': '/api/universities/*',
                'professors': '/api/professors/*',
                'applications': '/api/applications/*',
                'emails': '/api/emails/*',
                'analytics': '/api/analytics/*',
                'user': '/api/user/*'
            }
        })

    app.logger.info('Application initialized successfully')
    return app


def register_blueprints(app):
    """Register all blueprints"""
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

    app.logger.info('All blueprints registered')


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

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Run the application
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)

    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   PhD Application Automator - Backend Server             ║
    ║   Version: 1.0.0                                         ║
    ╠═══════════════════════════════════════════════════════════╣
    ║   Server running on: http://{host}:{port}                    ║
    ║   API Documentation: http://{host}:{port}/api                ║
    ║   Health Check: http://{host}:{port}/health                  ║
    ╠═══════════════════════════════════════════════════════════╣
    ║   Press CTRL+C to stop the server                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    app.run(host=host, port=port, debug=debug)
