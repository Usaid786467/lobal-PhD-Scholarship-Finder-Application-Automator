"""
University model for storing university information
"""
from datetime import datetime
from models.database import db
import json


class University(db.Model):
    """University model for storing university data"""

    __tablename__ = 'universities'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Basic Information
    name = db.Column(db.String(200), nullable=False, index=True)
    country = db.Column(db.String(100), nullable=False, index=True)
    city = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    domain = db.Column(db.String(100), nullable=True)  # e.g., mit.edu, tsinghua.edu.cn

    # Ranking (optional)
    ranking = db.Column(db.Integer, nullable=True)

    # Scholarship Information
    has_scholarship = db.Column(db.Boolean, default=False, nullable=False, index=True)
    scholarship_details = db.Column(db.Text, nullable=True)

    # Application Details
    application_deadline = db.Column(db.Date, nullable=True)

    # Research Areas (stored as JSON array)
    research_areas = db.Column(db.Text, nullable=True)  # JSON string

    # Contact Information
    contact_email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # Additional Info
    logo_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_scraped = db.Column(db.DateTime, nullable=True)

    # Relationships
    professors = db.relationship('Professor', backref='university', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='university', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, country, **kwargs):
        """Initialize university with required fields"""
        self.name = name
        self.country = country
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_research_areas(self, areas):
        """Set research areas from list"""
        if isinstance(areas, list):
            self.research_areas = json.dumps(areas)
        elif isinstance(areas, str):
            self.research_areas = areas

    def get_research_areas(self):
        """Get research areas as list"""
        if self.research_areas:
            try:
                return json.loads(self.research_areas)
            except:
                return []
        return []

    def update_last_scraped(self):
        """Update last scraped timestamp"""
        self.last_scraped = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self, include_professors=False):
        """Convert university to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'website': self.website,
            'domain': self.domain,
            'ranking': self.ranking,
            'has_scholarship': self.has_scholarship,
            'scholarship_details': self.scholarship_details,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'research_areas': self.get_research_areas(),
            'contact_email': self.contact_email,
            'phone': self.phone,
            'address': self.address,
            'logo_url': self.logo_url,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
            'professor_count': self.professors.count()
        }

        if include_professors:
            data['professors'] = [prof.to_dict() for prof in self.professors.all()]

        return data

    def __repr__(self):
        """String representation"""
        return f'<University {self.name}, {self.country}>'
