"""
API Routes Package
Exports all route blueprints
"""
from .auth import auth_bp
from .universities import universities_bp
from .professors import professors_bp
from .emails import emails_bp
from .applications import applications_bp
from .analytics import analytics_bp

__all__ = ['auth_bp', 'universities_bp', 'professors_bp', 'emails_bp', 'applications_bp', 'analytics_bp']
