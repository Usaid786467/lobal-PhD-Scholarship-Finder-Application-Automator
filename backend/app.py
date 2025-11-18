"""
PhD Application Automation System - Main Flask Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config
from models import db
import os

# Import blueprints
from routes import (
    auth_bp,
    universities_bp,
    professors_bp,
    emails_bp,
    applications_bp,
    analytics_bp
)


def create_app(config_name=None):
    """
    Application factory pattern
    Args:
        config_name: Configuration name (development, production, testing)
    Returns:
        Flask app instance
    """
    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(universities_bp)
    app.register_blueprint(professors_bp)
    app.register_blueprint(emails_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(analytics_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'PhD Application Automation System',
            'version': '1.0.0'
        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint"""
        return jsonify({
            'message': 'PhD Application Automation System API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'universities': '/api/universities',
                'professors': '/api/professors',
                'emails': '/api/emails',
                'applications': '/api/applications',
                'analytics': '/api/analytics'
            }
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({'error': 'Missing or invalid token'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    # Run app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  PhD Application Automation System                            ║
║  Backend Server Starting...                                   ║
║                                                               ║
║  Server: http://localhost:{port}                                ║
║  Environment: {os.getenv('FLASK_ENV', 'development').upper()}                                      ║
║                                                               ║
║  API Endpoints:                                               ║
║  - Auth:         /api/auth/*                                  ║
║  - Universities: /api/universities/*                          ║
║  - Professors:   /api/professors/*                            ║
║  - Emails:       /api/emails/*                                ║
║  - Applications: /api/applications/*                          ║
║  - Analytics:    /api/analytics/*                             ║
╚══════════════════════════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
