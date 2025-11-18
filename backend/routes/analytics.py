"""
Analytics Routes for PhD Application Automator
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_session, Application, Email, University, Professor, ApplicationStatus, EmailStatus
from sqlalchemy import func, extract
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        # Total counts
        universities_count = session.query(University).filter_by(is_active=True).count()
        professors_count = session.query(Professor).filter_by(is_active=True).count()
        applications_count = session.query(Application).filter_by(user_id=user_id).count()
        emails_sent = session.query(Email).filter_by(user_id=user_id).filter(
            Email.status.in_([EmailStatus.SENT, EmailStatus.DELIVERED, EmailStatus.OPENED, EmailStatus.REPLIED])
        ).count()

        # Response metrics
        emails_replied = session.query(Email).filter_by(
            user_id=user_id,
            status=EmailStatus.REPLIED
        ).count()

        response_rate = (emails_replied / emails_sent * 100) if emails_sent > 0 else 0

        # Recent activity
        recent_applications = session.query(Application).filter_by(
            user_id=user_id
        ).order_by(Application.created_at.desc()).limit(5).all()

        return jsonify({
            'stats': {
                'universities_discovered': universities_count,
                'professors_found': professors_count,
                'applications_submitted': applications_count,
                'emails_sent': emails_sent,
                'emails_replied': emails_replied,
                'response_rate': round(response_rate, 2)
            },
            'recent_applications': [a.to_dict(include_details=False) for a in recent_applications]
        }), 200

    except Exception as e:
        current_app.logger.error(f'Dashboard stats error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/by-country', methods=['GET'])
@jwt_required()
def get_applications_by_country():
    """Get applications grouped by country"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        # Query applications joined with universities
        results = session.query(
            University.country,
            func.count(Application.id).label('count')
        ).join(
            Application, Application.university_id == University.id
        ).filter(
            Application.user_id == user_id
        ).group_by(
            University.country
        ).order_by(
            func.count(Application.id).desc()
        ).all()

        data = [{'country': country, 'count': count} for country, count in results]

        return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/response-rate', methods=['GET'])
@jwt_required()
def get_response_rate_over_time():
    """Get email response rate over time"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        # Get emails grouped by week
        sent_by_week = session.query(
            func.date_trunc('week', Email.sent_at).label('week'),
            func.count(Email.id).label('sent')
        ).filter(
            Email.user_id == user_id,
            Email.sent_at.isnot(None)
        ).group_by('week').all()

        replied_by_week = session.query(
            func.date_trunc('week', Email.sent_at).label('week'),
            func.count(Email.id).label('replied')
        ).filter(
            Email.user_id == user_id,
            Email.status == EmailStatus.REPLIED
        ).group_by('week').all()

        # Combine data
        sent_dict = {str(week): count for week, count in sent_by_week}
        replied_dict = {str(week): count for week, count in replied_by_week}

        data = []
        for week in sent_dict:
            sent = sent_dict[week]
            replied = replied_dict.get(week, 0)
            rate = (replied / sent * 100) if sent > 0 else 0

            data.append({
                'week': week,
                'sent': sent,
                'replied': replied,
                'rate': round(rate, 2)
            })

        return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/success-funnel', methods=['GET'])
@jwt_required()
def get_success_funnel():
    """Get application success funnel"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        # Count applications at each stage
        draft = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.DRAFT
        ).count()

        sent = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.SENT
        ).count()

        opened = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.OPENED
        ).count()

        replied = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.REPLIED
        ).count()

        accepted = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.ACCEPTED
        ).count()

        funnel = [
            {'stage': 'Draft', 'count': draft},
            {'stage': 'Sent', 'count': sent},
            {'stage': 'Opened', 'count': opened},
            {'stage': 'Replied', 'count': replied},
            {'stage': 'Accepted', 'count': accepted}
        ]

        return jsonify({'funnel': funnel}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
