"""
User Model for PhD Application Automator
Handles user authentication and profile management
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model for authentication and profile management"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    # Profile Information
    research_interests = Column(JSON, default=list)  # List of research areas
    target_countries = Column(JSON, default=list)  # List of target countries
    education_background = Column(Text)  # Current degree, institution, etc.
    target_degree = Column(String(255))  # PhD in Mechanical Engineering, etc.

    # Documents
    cv_path = Column(String(500))  # Path to uploaded CV
    cv_filename = Column(String(255))  # Original filename
    cv_uploaded_at = Column(DateTime)  # Upload timestamp

    # Preferences
    preferences = Column(JSON, default=dict)  # User preferences and settings

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, email, password, name, **kwargs):
        """Initialize user with hashed password"""
        self.email = email.lower()
        self.set_password(password)
        self.name = name
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'research_interests': self.research_interests or [],
            'target_countries': self.target_countries or [],
            'education_background': self.education_background,
            'target_degree': self.target_degree,
            'cv_filename': self.cv_filename,
            'cv_uploaded_at': self.cv_uploaded_at.isoformat() if self.cv_uploaded_at else None,
            'preferences': self.preferences or {},
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }

        if include_sensitive:
            data['is_admin'] = self.is_admin
            data['cv_path'] = self.cv_path

        return data

    def __repr__(self):
        return f'<User {self.email}>'
