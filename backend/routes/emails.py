"""
Emails Routes
API endpoints for email generation and batch management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Email, EmailBatch, Application, Professor, User
from services.ai import GeminiService, EmailGenerator
from services.email import BatchManager, SMTPService
from config import Config
import json

emails_bp = Blueprint('emails', __name__, url_prefix='/api/emails')


@emails_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_emails():
    """
    Generate emails for selected professors
    POST /api/emails/generate
    Body: {professor_ids: [1, 2, 3]}
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json() or {}
        professor_ids = data.get('professor_ids', [])

        if not professor_ids:
            return jsonify({'error': 'professor_ids is required'}), 400

        # Get professors
        professors = Professor.query.filter(Professor.id.in_(professor_ids)).all()

        if not professors:
            return jsonify({'error': 'No professors found'}), 404

        # Initialize AI services
        gemini = GeminiService(Config.GEMINI_API_KEY)
        email_gen = EmailGenerator(gemini)

        # Generate emails
        emails_data = []
        for professor in professors:
            # Create or get application
            application = Application.query.filter_by(
                user_id=user_id,
                professor_id=professor.id
            ).first()

            if not application:
                application = Application(
                    user_id=user_id,
                    professor_id=professor.id,
                    status='draft'
                )
                db.session.add(application)
                db.session.flush()

            # Generate email
            email_content = email_gen.generate_email(
                professor_name=professor.name,
                professor_research=professor.research_interests or '[]',
                university_name=professor.university.name if professor.university else 'University',
                user_name=user.name,
                user_research=user.research_interests or 'Engineering',
                user_background="Master's student in Mechanical Engineering"
            )

            emails_data.append({
                'application_id': application.id,
                'subject': email_content['subject'],
                'body': email_content['body']
            })

        db.session.commit()

        # Create batch
        batch_manager = BatchManager()
        batch = batch_manager.create_batch(user_id, emails_data)

        if not batch:
            return jsonify({'error': 'Failed to create batch'}), 500

        return jsonify({
            'message': f'Generated {len(emails_data)} emails',
            'batch_id': batch.id,
            'count': len(emails_data)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/batches', methods=['GET'])
@jwt_required()
def get_batches():
    """Get user's email batches"""
    try:
        user_id = get_jwt_identity()
        batch_manager = BatchManager()

        batches = batch_manager.get_user_batches(user_id, limit=50)
        return jsonify({
            'batches': [batch.to_dict() for batch in batches]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/batches/<int:batch_id>', methods=['GET'])
@jwt_required()
def get_batch(batch_id):
    """Get batch details with emails"""
    try:
        user_id = get_jwt_identity()
        batch_manager = BatchManager()

        batch = batch_manager.get_batch(batch_id)
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404

        if batch.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        emails = batch_manager.get_batch_emails(batch_id)

        return jsonify({
            'batch': batch.to_dict(),
            'emails': [email.to_dict() for email in emails]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/batches/<int:batch_id>/approve', methods=['POST'])
@jwt_required()
def approve_batch(batch_id):
    """Approve batch for sending"""
    try:
        user_id = get_jwt_identity()
        batch_manager = BatchManager()

        batch = batch_manager.get_batch(batch_id)
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404

        if batch.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        success = batch_manager.approve_batch(batch_id)
        if not success:
            return jsonify({'error': 'Failed to approve batch'}), 500

        return jsonify({'message': 'Batch approved successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/batches/<int:batch_id>/send', methods=['POST'])
@jwt_required()
def send_batch(batch_id):
    """Send approved batch"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        batch_manager = BatchManager()

        batch = batch_manager.get_batch(batch_id)
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404

        if batch.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        if batch.status != 'approved':
            return jsonify({'error': 'Batch must be approved before sending'}), 400

        # Initialize SMTP service
        smtp = SMTPService(
            smtp_host=Config.SMTP_HOST,
            smtp_port=Config.SMTP_PORT,
            smtp_user=Config.SMTP_USER,
            smtp_password=Config.SMTP_PASSWORD,
            from_name=user.name
        )

        # Get emails to send
        emails = batch_manager.get_batch_emails(batch_id, status='approved')

        # Update batch status
        batch.status = 'sending'
        db.session.commit()

        # Send emails
        sent_count = 0
        failed_count = 0

        for email in emails:
            # Get professor email
            application = Application.query.get(email.application_id)
            if not application or not application.professor:
                continue

            to_email = application.professor.email

            # Attach CV if available
            attachments = [user.cv_path] if user.cv_path else None

            # Send email
            success = smtp.send_email(
                to_email=to_email,
                subject=email.subject,
                body=email.body,
                attachments=attachments
            )

            if success:
                batch_manager.mark_email_sent(email.id)
                sent_count += 1
            else:
                batch_manager.mark_email_failed(email.id, 'SMTP send failed')
                failed_count += 1

        return jsonify({
            'message': f'Batch sending completed. Sent: {sent_count}, Failed: {failed_count}',
            'sent': sent_count,
            'failed': failed_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@emails_bp.route('/<int:email_id>', methods=['PUT'])
@jwt_required()
def update_email(email_id):
    """Update email draft"""
    try:
        user_id = get_jwt_identity()
        email = Email.query.get(email_id)

        if not email:
            return jsonify({'error': 'Email not found'}), 404

        if email.batch.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        if email.status not in ['draft', 'approved']:
            return jsonify({'error': 'Cannot edit sent emails'}), 400

        data = request.get_json() or {}

        if 'subject' in data:
            email.subject = data['subject']
        if 'body' in data:
            email.body = data['body']

        db.session.commit()

        return jsonify({
            'message': 'Email updated successfully',
            'email': email.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
