"""
Database models package
Exports all models for easy importing
"""
from models.database import db, init_db, create_tables, drop_tables, reset_db
from models.user import User
from models.university import University
from models.professor import Professor
from models.application import Application
from models.email import Email, EmailBatch
from models.analytics import Analytics, ScrapingJob

__all__ = [
    'db',
    'init_db',
    'create_tables',
    'drop_tables',
    'reset_db',
    'User',
    'University',
    'Professor',
    'Application',
    'Email',
    'EmailBatch',
    'Analytics',
    'ScrapingJob'
]
