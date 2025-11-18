"""
Configuration Management for PhD Application Automator
This module handles all application configuration settings.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///phd_applications.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # Log SQL queries in debug mode

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # CORS Configuration
    CORS_ORIGINS = [os.getenv('FRONTEND_URL', 'http://localhost:3000')]
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

    # Email Configuration
    MAIL_SERVER = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('SMTP_PORT', 587))
    MAIL_USE_TLS = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('SMTP_USERNAME')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_FROM')
    MAIL_DEFAULT_SENDER_NAME = os.getenv('EMAIL_FROM_NAME', 'PhD Applicant')

    # Alternative Email Providers
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')

    # Email Limits
    DAILY_EMAIL_LIMIT = int(os.getenv('DAILY_EMAIL_LIMIT', 10000))
    HOURLY_EMAIL_LIMIT = int(os.getenv('HOURLY_EMAIL_LIMIT', 500))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 50))
    MIN_SEND_INTERVAL = int(os.getenv('MIN_SEND_INTERVAL', 5))

    # Redis Configuration (Celery)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', 0.7))
    GEMINI_MAX_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', 2048))

    # Web Scraping Configuration
    USER_AGENT = os.getenv('USER_AGENT',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    SCRAPING_DELAY = int(os.getenv('SCRAPING_DELAY', 2))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    PROXY_URL = os.getenv('PROXY_URL')

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,doc,docx').split(','))

    # Pagination
    RESULTS_PER_PAGE = int(os.getenv('RESULTS_PER_PAGE', 50))

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))

    # User Profile Configuration
    MY_NAME = os.getenv('MY_NAME', 'PhD Applicant')
    MY_EMAIL = os.getenv('MY_EMAIL')
    MY_RESEARCH_INTERESTS = os.getenv('MY_RESEARCH_INTERESTS', '').split(',')
    MY_DEGREE = os.getenv('MY_DEGREE', "Master's in Mechanical Engineering")
    MY_TARGET_DEGREE = os.getenv('MY_TARGET_DEGREE', 'PhD in Mechanical Engineering')

    # Target Countries
    TARGET_COUNTRIES = os.getenv('TARGET_COUNTRIES', 'USA,UK,Canada').split(',')

    # Feature Flags
    ENABLE_AUTO_SCRAPING = os.getenv('ENABLE_AUTO_SCRAPING', 'True').lower() == 'true'
    ENABLE_AUTO_EMAIL = os.getenv('ENABLE_AUTO_EMAIL', 'False').lower() == 'true'
    ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'True').lower() == 'true'
    ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'True').lower() == 'true'

    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

        # Log configuration status
        if app.debug:
            print("🔧 Configuration loaded successfully")
            print(f"   Environment: {Config.ENVIRONMENT}")
            print(f"   Database: {Config.SQLALCHEMY_DATABASE_URI.split('/')[-1]}")
            print(f"   Debug Mode: {Config.DEBUG}")


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False

    # Override with production database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/phd_db')

    # Stricter security in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
