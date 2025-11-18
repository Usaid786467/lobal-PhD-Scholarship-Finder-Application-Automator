"""
Analytics Routes
API endpoints for analytics and statistics
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Application, Email, EmailBatch, University, Professor
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get dashboard analytics"""
    try:
        user_id = get_jwt_identity()

        # Application stats
        total_applications = Application.query.filter_by(user_id=user_id).count()
        sent_applications = Application.query.filter_by(user_id=user_id, status='sent').count()
        replied_applications = Application.query.filter_by(user_id=user_id, status='replied').count()

        # Email stats
        total_emails = db.session.query(Email).join(EmailBatch).filter(
            EmailBatch.user_id == user_id
        ).count()

        sent_emails = db.session.query(Email).join(EmailBatch).filter(
            EmailBatch.user_id == user_id,
            Email.status == 'sent'
        ).count()

        # Response rate
        response_rate = (replied_applications / sent_applications * 100) if sent_applications > 0 else 0

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_applications = Application.query.filter_by(user_id=user_id).filter(
            Application.created_at >= thirty_days_ago
        ).count()

        # Applications by status
        apps_by_status = db.session.query(
            Application.status,
            db.func.count(Application.id)
        ).filter_by(user_id=user_id).group_by(Application.status).all()

        return jsonify({
            'total_applications': total_applications,
            'sent_applications': sent_applications,
            'replied_applications': replied_applications,
            'total_emails': total_emails,
            'sent_emails': sent_emails,
            'response_rate': round(response_rate, 2),
            'recent_activity': recent_applications,
            'applications_by_status': {status: count for status, count in apps_by_status}
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/timeline', methods=['GET'])
@jwt_required()
def get_timeline():
    """Get application timeline data"""
    try:
        user_id = get_jwt_identity()
        days = int(request.args.get('days', 30))

        start_date = datetime.utcnow() - timedelta(days=days)

        # Applications over time
        applications = db.session.query(
            db.func.date(Application.created_at).label('date'),
            db.func.count(Application.id).label('count')
        ).filter_by(user_id=user_id).filter(
            Application.created_at >= start_date
        ).group_by(db.func.date(Application.created_at)).all()

        timeline_data = [
            {
                'date': date.isoformat() if date else None,
                'count': count
            }
            for date, count in applications
        ]

        return jsonify({'timeline': timeline_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/universities', methods=['GET'])
@jwt_required()
def get_university_stats():
    """Get global university statistics"""
    try:
        total_universities = University.query.count()
        universities_by_country = db.session.query(
            University.country,
            db.func.count(University.id)
        ).group_by(University.country).all()

        with_scholarships = University.query.filter_by(has_scholarship=True).count()

        return jsonify({
            'total_universities': total_universities,
            'by_country': {country: count for country, count in universities_by_country},
            'with_scholarships': with_scholarships
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/professors', methods=['GET'])
@jwt_required()
def get_professor_stats():
    """Get global professor statistics"""
    try:
        total_professors = Professor.query.count()
        accepting_students = Professor.query.filter_by(accepting_students=True).count()

        by_department = db.session.query(
            Professor.department,
            db.func.count(Professor.id)
        ).group_by(Professor.department).all()

        return jsonify({
            'total_professors': total_professors,
            'accepting_students': accepting_students,
            'by_department': {dept: count for dept, count in by_department if dept}
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
