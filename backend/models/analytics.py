"""
Analytics Model
Stores analytics and metrics data
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey
from . import db


class Analytics(db.Model):
    """Analytics model for storing metrics and statistics"""

    __tablename__ = 'analytics'

    # Primary Key
    id = Column(Integer, primary_key=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    # Metric Information
    metric_name = Column(String(200), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50))  # count, percentage, seconds, etc.

    # Category
    category = Column(String(100), index=True)  # email, application, scraping, etc.
    subcategory = Column(String(100))

    # Time Period
    date = Column(Date, nullable=False, index=True)
    hour = Column(Integer)  # 0-23 for hourly metrics

    # Additional Data
    extra_data = Column(JSON)  # Additional contextual data
    dimensions = Column(JSON)  # Breakdown dimensions (country, university, etc.)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert analytics to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_unit': self.metric_unit,
            'category': self.category,
            'subcategory': self.subcategory,
            'date': self.date.isoformat() if self.date else None,
            'hour': self.hour,
            'extra_data': self.extra_data or {},
            'dimensions': self.dimensions or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def record_metric(user_id, metric_name, value, category=None, extra_data=None, date=None):
        """Helper method to record a metric"""
        from datetime import date as date_type

        metric = Analytics(
            user_id=user_id,
            metric_name=metric_name,
            metric_value=value,
            category=category,
            date=date or date_type.today(),
            extra_data=extra_data or {}
        )
        db.session.add(metric)
        db.session.commit()
        return metric

    def __repr__(self):
        return f'<Analytics {self.metric_name}: {self.metric_value}>'
