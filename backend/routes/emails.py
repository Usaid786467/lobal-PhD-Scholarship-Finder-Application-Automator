"""
Email Routes for PhD Application Automator
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_session, Email, EmailBatch, EmailStatus
from datetime import datetime

emails_bp = Blueprint('emails', __name__)


@emails_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_emails():
    """Generate batch of personalized emails using AI"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        professor_ids = data.get('professor_ids', [])

        if not professor_ids:
            return jsonify({'error': 'No professors selected'}), 400

        # TODO: Implement AI email generation
        # For now, return placeholder
        return jsonify({
            'message': f'Generating {len(professor_ids)} emails',
            'job_id': 'placeholder-job-id',
            'count': len(professor_ids)
        }), 202

    except Exception as e:
        current_app.logger.error(f'Email generation error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/drafts', methods=['GET'])
@jwt_required()
def get_draft_emails():
    """Get draft emails"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        drafts = session.query(Email).filter_by(
            user_id=user_id,
            status=EmailStatus.DRAFT
        ).order_by(Email.created_at.desc()).all()

        return jsonify({
            'drafts': [e.to_dict(include_body=False) for e in drafts],
            'count': len(drafts)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/<int:email_id>', methods=['GET'])
@jwt_required()
def get_email(email_id):
    """Get email details"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        email = session.query(Email).filter_by(
            id=email_id,
            user_id=user_id
        ).first()

        if not email:
            return jsonify({'error': 'Email not found'}), 404

        return jsonify({'email': email.to_dict(include_body=True)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/<int:email_id>', methods=['PUT'])
@jwt_required()
def update_email(email_id):
    """Update email draft"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        session = get_session()
        email = session.query(Email).filter_by(
            id=email_id,
            user_id=user_id
        ).first()

        if not email:
            return jsonify({'error': 'Email not found'}), 404

        # Update allowed fields
        if 'subject' in data:
            email.subject = data['subject']
        if 'body' in data:
            email.body = data['body']
        if 'notes' in data:
            email.notes = data['notes']

        session.commit()

        return jsonify({
            'message': 'Email updated successfully',
            'email': email.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/batch/approve', methods=['POST'])
@jwt_required()
def approve_batch():
    """Approve batch of emails for sending"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        email_ids = data.get('email_ids', [])

        if not email_ids:
            return jsonify({'error': 'No emails selected'}), 400

        session = get_session()

        # Approve all selected emails
        for email_id in email_ids:
            email = session.query(Email).filter_by(
                id=email_id,
                user_id=user_id
            ).first()

            if email:
                email.approve(user_id)

        session.commit()

        return jsonify({
            'message': f'{len(email_ids)} emails approved',
            'count': len(email_ids)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/batch/send', methods=['POST'])
@jwt_required()
def send_batch():
    """Send approved batch of emails"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        batch_id = data.get('batch_id')

        # TODO: Trigger email sending task
        return jsonify({
            'message': 'Email sending started',
            'batch_id': batch_id
        }), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/history', methods=['GET'])
@jwt_required()
def get_email_history():
    """Get email history"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        query = session.query(Email).filter_by(user_id=user_id)
        query = query.filter(Email.status.in_([EmailStatus.SENT, EmailStatus.DELIVERED, EmailStatus.OPENED, EmailStatus.REPLIED]))
        query = query.order_by(Email.sent_at.desc())

        total = query.count()
        emails = query.offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            'emails': [e.to_dict(include_body=False) for e in emails],
            'total': total,
            'page': page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
