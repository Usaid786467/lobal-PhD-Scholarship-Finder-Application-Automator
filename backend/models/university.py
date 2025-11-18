"""
University Model
Represents a university with PhD programs
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, Date
from . import db


class University(db.Model):
    """University model for storing university information"""

    __tablename__ = 'universities'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Basic Information
    name = Column(String(500), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    city = Column(String(200))
    state_province = Column(String(200))

    # Contact Information
    website = Column(String(500))
    domain = Column(String(200), index=True)  # e.g., .cn for Chinese universities
    contact_email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)

    # University Details
    ranking = Column(Integer)  # Optional world ranking
    logo_url = Column(String(500))
    type = Column(String(100))  # Public, Private, etc.

    # Research Information
    research_areas = Column(JSON)  # List of research areas offered
    departments = Column(JSON)  # List of departments

    # Scholarship Information
    has_scholarship = Column(Boolean, default=False, index=True)
    scholarship_details = Column(Text)
    scholarship_amount = Column(String(200))
    scholarship_url = Column(String(500))

    # Application Information
    application_deadline = Column(Date, index=True)
    application_requirements = Column(JSON)  # List of requirements
    application_url = Column(String(500))
    accepts_international = Column(Boolean, default=True)
    language_requirements = Column(JSON)  # TOEFL, IELTS scores, etc.

    # Metadata
    description = Column(Text)
    notes = Column(Text)

    # Scraping Information
    last_scraped = Column(DateTime)
    scraping_status = Column(String(50))  # success, failed, partial
    scraping_error = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    professors = db.relationship('Professor', backref='university', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='university', lazy='dynamic')

    def to_dict(self, include_professors=False):
        """Convert university to dictionary"""
        university_dict = {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'state_province': self.state_province,
            'website': self.website,
            'domain': self.domain,
            'contact_email': self.contact_email,
            'phone': self.phone,
            'address': self.address,
            'ranking': self.ranking,
            'logo_url': self.logo_url,
            'type': self.type,
            'research_areas': self.research_areas or [],
            'departments': self.departments or [],
            'has_scholarship': self.has_scholarship,
            'scholarship_details': self.scholarship_details,
            'scholarship_amount': self.scholarship_amount,
            'scholarship_url': self.scholarship_url,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'application_requirements': self.application_requirements or [],
            'application_url': self.application_url,
            'accepts_international': self.accepts_international,
            'language_requirements': self.language_requirements or {},
            'description': self.description,
            'notes': self.notes,
            'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'professor_count': self.professors.count() if hasattr(self, 'professors') else 0,
        }

        if include_professors:
            university_dict['professors'] = [p.to_dict() for p in self.professors.all()]

        return university_dict

    def __repr__(self):
        return f'<University {self.name}, {self.country}>'
