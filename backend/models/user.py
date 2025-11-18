"""
User model for authentication and profile management
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
import json


class User(db.Model):
    """User model for storing user account information"""

    __tablename__ = 'users'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile Information
    name = db.Column(db.String(100), nullable=False)

    # Research Interests (stored as JSON)
    research_interests = db.Column(db.Text, nullable=True)  # JSON string

    # Target Countries (stored as JSON)
    target_countries = db.Column(db.Text, nullable=True)  # JSON string

    # User Preferences (stored as JSON)
    preferences = db.Column(db.Text, nullable=True)  # JSON string

    # CV Path
    cv_path = db.Column(db.String(255), nullable=True)

    # Account Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    applications = db.relationship('Application', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    email_batches = db.relationship('EmailBatch', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, email, password, name, research_interests=None, target_countries=None):
        """Initialize user with required fields"""
        self.email = email
        self.set_password(password)
        self.name = name
        if research_interests:
            self.set_research_interests(research_interests)
        if target_countries:
            self.set_target_countries(target_countries)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def set_research_interests(self, interests):
        """Set research interests from list"""
        if isinstance(interests, list):
            self.research_interests = json.dumps(interests)
        elif isinstance(interests, str):
            self.research_interests = interests

    def get_research_interests(self):
        """Get research interests as list"""
        if self.research_interests:
            try:
                return json.loads(self.research_interests)
            except:
                return []
        return []

    def set_target_countries(self, countries):
        """Set target countries from list"""
        if isinstance(countries, list):
            self.target_countries = json.dumps(countries)
        elif isinstance(countries, str):
            self.target_countries = countries

    def get_target_countries(self):
        """Get target countries as list"""
        if self.target_countries:
            try:
                return json.loads(self.target_countries)
            except:
                return []
        return []

    def set_preferences(self, prefs):
        """Set preferences from dictionary"""
        if isinstance(prefs, dict):
            self.preferences = json.dumps(prefs)
        elif isinstance(prefs, str):
            self.preferences = prefs

    def get_preferences(self):
        """Get preferences as dictionary"""
        if self.preferences:
            try:
                return json.loads(self.preferences)
            except:
                return {}
        return {}

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'research_interests': self.get_research_interests(),
            'target_countries': self.get_target_countries(),
            'preferences': self.get_preferences(),
            'cv_path': self.cv_path,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

        if include_sensitive:
            data['password_hash'] = self.password_hash

        return data

    def __repr__(self):
        """String representation"""
        return f'<User {self.email}>'
