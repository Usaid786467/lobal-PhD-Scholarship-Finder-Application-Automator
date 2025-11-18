"""
Application configuration management
Loads configuration from environment variables
"""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = Path(__file__).parent
load_dotenv(basedir / '.env')


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{basedir / "phd_applications.db"}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # CORS Configuration
    CORS_ORIGINS = os.getenv('FRONTEND_URL', 'http://localhost:3000').split(',')
    CORS_SUPPORTS_CREDENTIALS = True

    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-pro'
    GEMINI_RATE_LIMIT = 60  # requests per minute

    # Email Configuration (SMTP)
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    EMAIL_FROM = os.getenv('EMAIL_FROM', '')
    EMAIL_FROM_NAME = os.getenv('EMAIL_FROM_NAME', 'PhD Applicant')

    # Alternative Email Services
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', '')

    # Email Sending Limits
    DAILY_EMAIL_LIMIT = int(os.getenv('DAILY_EMAIL_LIMIT', 10000))
    HOURLY_EMAIL_LIMIT = int(os.getenv('HOURLY_EMAIL_LIMIT', 500))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 50))
    MIN_SEND_INTERVAL = int(os.getenv('MIN_SEND_INTERVAL', 5))

    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)

    # Web Scraping Configuration
    USER_AGENT = os.getenv(
        'USER_AGENT',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    SCRAPING_DELAY = int(os.getenv('SCRAPING_DELAY', 2))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    PROXY_URL = os.getenv('PROXY_URL', '')

    # Selenium Configuration
    WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH', '/usr/local/bin/chromedriver')
    HEADLESS_BROWSER = os.getenv('HEADLESS_BROWSER', 'True').lower() == 'true'

    # File Upload Configuration
    UPLOAD_FOLDER = basedir / os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = set(
        os.getenv('ALLOWED_EXTENSIONS', 'pdf,doc,docx').split(',')
    )

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = basedir / os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', 10 * 1024 * 1024))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))

    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'redis://localhost:6379/1')

    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))

    # Data Directories
    DATA_DIR = basedir / os.getenv('DATA_DIR', 'data')
    BACKUP_DIR = basedir / os.getenv('BACKUP_DIR', 'backups')

    # Scraping Targets
    SCRAPE_COUNTRIES = os.getenv(
        'SCRAPE_COUNTRIES',
        'USA,UK,Canada,Germany,Australia,China,Singapore'
    ).split(',')
    RESEARCH_AREAS = os.getenv(
        'RESEARCH_AREAS',
        'Deep Learning,Machine Learning,Manufacturing,Aerospace,Computer Vision'
    ).split(',')

    # Feature Flags
    ENABLE_EMAIL_SENDING = os.getenv('ENABLE_EMAIL_SENDING', 'True').lower() == 'true'
    ENABLE_AUTO_SCRAPING = os.getenv('ENABLE_AUTO_SCRAPING', 'False').lower() == 'true'
    ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'True').lower() == 'true'
    ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'True').lower() == 'true'

    # Sentry Configuration
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')
    SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT', 'development')

    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.BACKUP_DIR, exist_ok=True)
        os.makedirs(Config.LOG_FILE.parent, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Initialize Sentry for error tracking
        if cls.SENTRY_DSN:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration

            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                integrations=[FlaskIntegration()],
                environment=cls.SENTRY_ENVIRONMENT,
                traces_sample_rate=0.1
            )


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration object"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    return config.get(config_name, DevelopmentConfig)
