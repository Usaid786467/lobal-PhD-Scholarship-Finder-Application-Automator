"""
Routes Package
API endpoints for the application
"""

from .auth import auth_bp
from .universities import universities_bp
from .professors import professors_bp
from .applications import applications_bp
from .emails import emails_bp
from .analytics import analytics_bp
from .user import user_bp

__all__ = [
    'auth_bp',
    'universities_bp',
    'professors_bp',
    'applications_bp',
    'emails_bp',
    'analytics_bp',
    'user_bp'
]
