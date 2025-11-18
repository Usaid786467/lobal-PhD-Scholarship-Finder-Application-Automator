"""
Models package for PhD Application Automator
Exports all database models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Import all models
from .user import User, Base as UserBase
from .university import University, Base as UniversityBase
from .professor import Professor, Base as ProfessorBase
from .application import Application, ApplicationStatus, Base as ApplicationBase
from .email import Email, EmailBatch, EmailStatus, Base as EmailBase
from .analytics import Analytics, ScrapingJob, Base as AnalyticsBase

# Use UserBase as the main Base (they all use declarative_base())
Base = UserBase

# Export all models
__all__ = [
    'User',
    'University',
    'Professor',
    'Application',
    'ApplicationStatus',
    'Email',
    'EmailBatch',
    'EmailStatus',
    'Analytics',
    'ScrapingJob',
    'Base',
    'init_db',
    'get_session',
]


# Database session management
_engine = None
_session_factory = None


def init_db(database_url, echo=False):
    """
    Initialize database connection and create tables

    Args:
        database_url: SQLAlchemy database URL
        echo: Whether to echo SQL queries (for debugging)

    Returns:
        SQLAlchemy engine
    """
    global _engine, _session_factory

    _engine = create_engine(database_url, echo=echo, pool_pre_ping=True)
    _session_factory = scoped_session(sessionmaker(bind=_engine))

    # Create all tables
    Base.metadata.create_all(_engine)

    return _engine


def get_session():
    """Get database session"""
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _session_factory()


def close_session():
    """Close database session"""
    if _session_factory:
        _session_factory.remove()
