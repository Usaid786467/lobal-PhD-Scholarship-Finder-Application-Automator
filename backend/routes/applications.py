"""
Application Routes for PhD Application Automator
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_session, Application, ApplicationStatus
from datetime import datetime

applications_bp = Blueprint('applications', __name__)


@applications_bp.route('', methods=['GET'])
@jwt_required()
def get_applications():
    """Get all applications for current user"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        query = session.query(Application).filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=ApplicationStatus(status))

        query = query.order_by(Application.created_at.desc())

        total = query.count()
        applications = query.offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            'applications': [a.to_dict(include_details=False) for a in applications],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get applications error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    """Get application details"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        application = session.query(Application).filter_by(
            id=application_id,
            user_id=user_id
        ).first()

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        return jsonify({'application': application.to_dict(include_details=True)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:application_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(application_id):
    """Update application status"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        new_status = data.get('status')
        notes = data.get('notes')

        session = get_session()
        application = session.query(Application).filter_by(
            id=application_id,
            user_id=user_id
        ).first()

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        application.update_status(new_status, notes)
        session.commit()

        return jsonify({
            'message': 'Status updated successfully',
            'application': application.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_application_stats():
    """Get application statistics"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        total = session.query(Application).filter_by(user_id=user_id).count()
        sent = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.SENT
        ).count()
        replied = session.query(Application).filter_by(
            user_id=user_id,
            status=ApplicationStatus.REPLIED
        ).count()

        return jsonify({
            'total': total,
            'sent': sent,
            'replied': replied,
            'response_rate': (replied / sent * 100) if sent > 0 else 0
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
