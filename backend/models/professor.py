"""
Professor Model
Represents a professor/faculty member
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from . import db


class Professor(db.Model):
    """Professor model for storing professor information"""

    __tablename__ = 'professors'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Foreign Key
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False, index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    title = Column(String(100))  # Professor, Associate Professor, etc.
    email = Column(String(255), index=True)
    phone = Column(String(50))

    # Academic Information
    department = Column(String(200))
    research_interests = Column(JSON)  # List of research interests
    specializations = Column(JSON)  # Specific areas of expertise

    # Research Metrics
    h_index = Column(Integer)
    citations = Column(Integer)
    publications_count = Column(Integer)
    publications = Column(JSON)  # List of recent publications

    # Student Information
    accepting_students = Column(Boolean, index=True)
    current_students_count = Column(Integer)
    graduated_students_count = Column(Integer)

    # Online Presence
    profile_url = Column(String(500))  # University profile page
    personal_website = Column(String(500))
    google_scholar_url = Column(String(500))
    research_gate_url = Column(String(500))
    linkedin_url = Column(String(500))

    # Lab Information
    lab_name = Column(String(255))
    lab_website = Column(String(500))
    lab_description = Column(Text)

    # Grants and Funding
    active_grants = Column(JSON)  # List of active grants
    total_funding = Column(String(200))

    # Contact Status
    last_contacted = Column(DateTime, index=True)
    contact_count = Column(Integer, default=0)
    response_received = Column(Boolean, default=False)

    # Matching Score (calculated by AI)
    match_score = Column(Float)  # 0-100 compatibility score
    match_reasons = Column(JSON)  # Reasons for the match

    # Metadata
    bio = Column(Text)
    photo_url = Column(String(500))
    notes = Column(Text)

    # Scraping Information
    last_scraped = Column(DateTime)
    scraping_status = Column(String(50))
    scraping_error = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='professor', lazy='dynamic')

    def to_dict(self, include_university=False):
        """Convert professor to dictionary"""
        professor_dict = {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'title': self.title,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'research_interests': self.research_interests or [],
            'specializations': self.specializations or [],
            'h_index': self.h_index,
            'citations': self.citations,
            'publications_count': self.publications_count,
            'publications': self.publications or [],
            'accepting_students': self.accepting_students,
            'current_students_count': self.current_students_count,
            'graduated_students_count': self.graduated_students_count,
            'profile_url': self.profile_url,
            'personal_website': self.personal_website,
            'google_scholar_url': self.google_scholar_url,
            'research_gate_url': self.research_gate_url,
            'linkedin_url': self.linkedin_url,
            'lab_name': self.lab_name,
            'lab_website': self.lab_website,
            'lab_description': self.lab_description,
            'active_grants': self.active_grants or [],
            'total_funding': self.total_funding,
            'last_contacted': self.last_contacted.isoformat() if self.last_contacted else None,
            'contact_count': self.contact_count,
            'response_received': self.response_received,
            'match_score': self.match_score,
            'match_reasons': self.match_reasons or [],
            'bio': self.bio,
            'photo_url': self.photo_url,
            'notes': self.notes,
            'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_university and self.university:
            professor_dict['university'] = self.university.to_dict()

        return professor_dict

    def __repr__(self):
        return f'<Professor {self.name}, {self.department}>'
