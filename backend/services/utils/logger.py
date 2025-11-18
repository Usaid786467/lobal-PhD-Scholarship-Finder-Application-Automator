"""
Logging configuration and utilities
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime


def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Setup logger with file and console handlers

    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers = []

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file specified)
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        os.makedirs(log_dir, exist_ok=True)

        # Rotating file handler (10MB max, 5 backups)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create default application logger
app_logger = setup_logger(
    'phd_app',
    log_file='logs/app.log',
    level=logging.INFO
)

# Create scraping logger
scraping_logger = setup_logger(
    'scraping',
    log_file='logs/scraping.log',
    level=logging.INFO
)

# Create email logger
email_logger = setup_logger(
    'email',
    log_file='logs/email.log',
    level=logging.INFO
)

# Create AI logger
ai_logger = setup_logger(
    'ai',
    log_file='logs/ai.log',
    level=logging.INFO
)


def log_exception(logger, exception, context=None):
    """
    Log exception with context

    Args:
        logger: Logger instance
        exception: Exception object
        context: Additional context (dict)
    """
    error_msg = f"Exception: {str(exception)}"
    if context:
        error_msg += f" | Context: {context}"
    logger.error(error_msg, exc_info=True)


def log_api_request(logger, method, endpoint, user_id=None, status_code=None):
    """
    Log API request

    Args:
        logger: Logger instance
        method: HTTP method
        endpoint: API endpoint
        user_id: User ID (optional)
        status_code: Response status code (optional)
    """
    log_msg = f"{method} {endpoint}"
    if user_id:
        log_msg += f" | User: {user_id}"
    if status_code:
        log_msg += f" | Status: {status_code}"
    logger.info(log_msg)
