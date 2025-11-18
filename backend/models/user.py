"""
User Model
Represents a user of the application
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from . import db


class User(db.Model):
    """User model for authentication and profile"""

    __tablename__ = 'users'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile Information
    name = Column(String(255), nullable=False)
    phone = Column(String(50))
    country = Column(String(100))

    # Research Profile
    research_interests = Column(JSON)  # List of research areas
    target_countries = Column(JSON)  # List of target countries
    preferences = Column(JSON)  # User preferences and settings

    # Documents
    cv_path = Column(String(500))  # Path to CV file
    cv_filename = Column(String(255))  # Original filename

    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    email_batches = db.relationship('EmailBatch', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, email, password, name, **kwargs):
        """Initialize user with email, password, and name"""
        self.email = email.lower().strip()
        self.set_password(password)
        self.name = name
        self.research_interests = kwargs.get('research_interests', [])
        self.target_countries = kwargs.get('target_countries', [])
        self.preferences = kwargs.get('preferences', {})

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        user_dict = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'country': self.country,
            'research_interests': self.research_interests or [],
            'target_countries': self.target_countries or [],
            'preferences': self.preferences or {},
            'cv_filename': self.cv_filename,
            'has_cv': bool(self.cv_path),
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }

        if include_sensitive:
            user_dict['cv_path'] = self.cv_path

        return user_dict

    def __repr__(self):
        return f'<User {self.email}>'
