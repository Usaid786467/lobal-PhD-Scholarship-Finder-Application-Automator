"""
Database Models Package
Exports all models for easy import
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .university import University
from .professor import Professor
from .application import Application
from .email import Email, EmailBatch

__all__ = ['db', 'User', 'University', 'Professor', 'Application', 'Email', 'EmailBatch']
