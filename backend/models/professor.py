"""
Professor Model for PhD Application Automator
Stores professor profiles and research information
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Professor(Base):
    """Professor model for storing faculty information"""

    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True)

    # University Association
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False, index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    title = Column(String(255))  # Professor, Associate Professor, Assistant Professor
    email = Column(String(255), index=True)  # Primary contact
    secondary_email = Column(String(255))
    phone = Column(String(50))

    # Department/Lab
    department = Column(String(500))
    lab_name = Column(String(500))
    lab_website = Column(String(500))
    office_location = Column(String(500))

    # Research Information
    research_interests = Column(JSON, default=list)  # List of research areas
    research_keywords = Column(JSON, default=list)  # Keywords from papers
    research_summary = Column(Text)  # AI-generated summary

    # Publications
    publications = Column(JSON, default=list)  # List of publication objects
    recent_publications = Column(JSON, default=list)  # Last 2 years
    total_publications = Column(Integer, default=0)
    h_index = Column(Integer)
    i10_index = Column(Integer)
    total_citations = Column(Integer)

    # Academic Profiles
    google_scholar_url = Column(String(500))
    google_scholar_id = Column(String(100))
    researchgate_url = Column(String(500))
    orcid = Column(String(100))
    linkedin_url = Column(String(500))
    personal_website = Column(String(500))
    profile_url = Column(String(500))  # University profile page

    # Student Information
    accepting_students = Column(Boolean, index=True)  # Currently accepting PhD students
    accepting_status_text = Column(String(500))  # e.g., "Accepting applications for Fall 2025"
    current_students = Column(JSON, default=list)  # List of current PhD students
    student_count = Column(Integer, default=0)
    graduated_students = Column(Integer, default=0)

    # Funding
    has_funding = Column(Boolean)
    funding_sources = Column(JSON, default=list)  # List of grants/funding sources
    active_grants = Column(JSON, default=list)

    # Contact Status
    last_contacted = Column(DateTime, index=True)
    contact_count = Column(Integer, default=0)  # How many times contacted
    response_received = Column(Boolean, default=False)
    response_date = Column(DateTime)
    response_type = Column(String(50))  # 'positive', 'negative', 'neutral'

    # Match Information
    match_score = Column(Float)  # 0-100 percentage
    match_reasons = Column(JSON, default=list)  # Why this professor matches

    # Scraping Metadata
    last_scraped = Column(DateTime)
    scraping_status = Column(String(50))  # 'pending', 'completed', 'failed'
    scraping_source = Column(String(100))  # 'google_scholar', 'university', 'researchgate'
    scraping_errors = Column(Text)

    # Photo/Image
    photo_url = Column(String(500))

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_favorited = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Notes
    notes = Column(Text)  # User's personal notes

    def to_dict(self, include_details=True):
        """Convert professor to dictionary"""
        data = {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'title': self.title,
            'email': self.email,
            'department': self.department,
            'research_interests': self.research_interests or [],
            'h_index': self.h_index,
            'total_citations': self.total_citations,
            'accepting_students': self.accepting_students,
            'match_score': self.match_score,
            'photo_url': self.photo_url,
            'last_contacted': self.last_contacted.isoformat() if self.last_contacted else None,
            'response_received': self.response_received,
            'is_favorited': self.is_favorited,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_details:
            data.update({
                'secondary_email': self.secondary_email,
                'phone': self.phone,
                'lab_name': self.lab_name,
                'lab_website': self.lab_website,
                'office_location': self.office_location,
                'research_keywords': self.research_keywords or [],
                'research_summary': self.research_summary,
                'publications': self.publications or [],
                'recent_publications': self.recent_publications or [],
                'total_publications': self.total_publications,
                'i10_index': self.i10_index,
                'google_scholar_url': self.google_scholar_url,
                'researchgate_url': self.researchgate_url,
                'orcid': self.orcid,
                'linkedin_url': self.linkedin_url,
                'personal_website': self.personal_website,
                'profile_url': self.profile_url,
                'accepting_status_text': self.accepting_status_text,
                'current_students': self.current_students or [],
                'student_count': self.student_count,
                'graduated_students': self.graduated_students,
                'has_funding': self.has_funding,
                'funding_sources': self.funding_sources or [],
                'active_grants': self.active_grants or [],
                'contact_count': self.contact_count,
                'response_type': self.response_type,
                'response_date': self.response_date.isoformat() if self.response_date else None,
                'match_reasons': self.match_reasons or [],
                'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
                'notes': self.notes,
            })

        return data

    def calculate_match_score(self, user_interests):
        """Calculate match score based on user research interests"""
        score = 0.0
        reasons = []

        # Research interest overlap (40 points)
        if self.research_interests and user_interests:
            user_areas_lower = [area.lower().strip() for area in user_interests]
            prof_areas_lower = [area.lower().strip() for area in self.research_interests]

            matches = []
            for user_area in user_areas_lower:
                for prof_area in prof_areas_lower:
                    if user_area in prof_area or prof_area in user_area:
                        matches.append(user_area)
                        break

            if matches:
                overlap_score = min(len(matches) * 13, 40)  # Max 40 points
                score += overlap_score
                reasons.append(f"Research overlap: {', '.join(matches[:3])}")

        # Academic metrics (30 points)
        if self.h_index:
            if self.h_index >= 50:
                score += 15
                reasons.append(f"High impact researcher (h-index: {self.h_index})")
            elif self.h_index >= 30:
                score += 10
            elif self.h_index >= 15:
                score += 5

        if self.total_citations:
            if self.total_citations >= 10000:
                score += 15
            elif self.total_citations >= 5000:
                score += 10
            elif self.total_citations >= 1000:
                score += 5

        # Recent publications (15 points)
        if self.recent_publications:
            pub_count = len(self.recent_publications)
            if pub_count >= 10:
                score += 15
                reasons.append(f"Very active researcher ({pub_count} recent publications)")
            elif pub_count >= 5:
                score += 10
            elif pub_count >= 2:
                score += 5

        # Currently accepting students (15 points)
        if self.accepting_students:
            score += 15
            reasons.append("Currently accepting PhD students")

        self.match_score = min(score, 100)  # Cap at 100
        self.match_reasons = reasons
        return self.match_score

    def record_contact(self):
        """Record that this professor was contacted"""
        self.last_contacted = datetime.utcnow()
        self.contact_count += 1

    def record_response(self, response_type='neutral'):
        """Record professor's response"""
        self.response_received = True
        self.response_date = datetime.utcnow()
        self.response_type = response_type

    def __repr__(self):
        return f'<Professor {self.name}>'
