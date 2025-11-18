"""
Logging Configuration
Centralized logging setup for the application
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(app):
    """Setup application logging"""

    # Get log configuration from app config
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    log_file = app.config.get('LOG_FILE', 'logs/app.log')
    max_size = app.config.get('LOG_MAX_SIZE', 10 * 1024 * 1024)  # 10MB
    backup_count = app.config.get('LOG_BACKUP_COUNT', 5)

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_size,
        backupCount=backup_count
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)

    # Set werkzeug logger level
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    app.logger.info('Logging configured successfully')


def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)
