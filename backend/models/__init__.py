"""
Database Models Package
Contains all SQLAlchemy models for the application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()


# Import all models for easy access
from .user import User
from .university import University
from .professor import Professor
from .application import Application
from .email import Email, EmailBatch
from .analytics import Analytics
from .scraping_job import ScrapingJob

__all__ = [
    'db',
    'User',
    'University',
    'Professor',
    'Application',
    'Email',
    'EmailBatch',
    'Analytics',
    'ScrapingJob'
]
