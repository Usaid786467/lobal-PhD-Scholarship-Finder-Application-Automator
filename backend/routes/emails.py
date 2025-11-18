"""
Email Routes
CRUD operations for emails and email batches
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, Email, EmailBatch, Application
from services.utils.validators import validate_required_fields


emails_bp = Blueprint('emails', __name__)


@emails_bp.route('/', methods=['GET'])
@jwt_required()
def get_emails():
    """Get list of emails with pagination and filtering"""
    try:
        user_id = get_jwt_identity()

        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # Max 100 items per page

        # Filter parameters
        status = request.args.get('status')
        batch_id = request.args.get('batch_id', type=int)
        application_id = request.args.get('application_id', type=int)

        # Build query - join with applications to filter by user
        query = Email.query.join(Application).filter(Application.user_id == user_id)

        if status:
            query = query.filter(Email.status == status)

        if batch_id:
            query = query.filter(Email.batch_id == batch_id)

        if application_id:
            query = query.filter(Email.application_id == application_id)

        # Order by created date (newest first)
        query = query.order_by(Email.created_at.desc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        include_body = request.args.get('include_body', 'false').lower() == 'true'

        return jsonify({
            'success': True,
            'emails': [email.to_dict(include_body=include_body) for email in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get emails error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve emails',
            'message': str(e)
        }), 500


@emails_bp.route('/<int:email_id>', methods=['GET'])
@jwt_required()
def get_email(email_id):
    """Get a single email by ID"""
    try:
        user_id = get_jwt_identity()

        # Join with application to verify ownership
        email = Email.query.join(Application).filter(
            Email.id == email_id,
            Application.user_id == user_id
        ).first()

        if not email:
            return jsonify({
                'success': False,
                'error': 'Email not found'
            }), 404

        return jsonify({
            'success': True,
            'email': email.to_dict(include_body=True)
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get email error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve email',
            'message': str(e)
        }), 500


@emails_bp.route('/', methods=['POST'])
@jwt_required()
def create_email():
    """Create a new email"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['application_id', 'to_email', 'subject', 'body'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Verify application belongs to user
        application = Application.query.filter_by(
            id=data['application_id'],
            user_id=user_id
        ).first()

        if not application:
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404

        # Create email
        email = Email(
            application_id=data['application_id'],
            batch_id=data.get('batch_id'),
            to_email=data['to_email'].strip(),
            to_name=data.get('to_name'),
            subject=data['subject'].strip(),
            body=data['body'],
            html_body=data.get('html_body'),
            template_id=data.get('template_id'),
            template_variables=data.get('template_variables', {}),
            attachments=data.get('attachments', []),
            status=data.get('status', Email.STATUS_DRAFT),
            priority=data.get('priority', 0),
            scheduled_time=data.get('scheduled_time')
        )

        db.session.add(email)
        db.session.commit()

        current_app.logger.info(f'Email created: {email.id} for application {application.id}')

        return jsonify({
            'success': True,
            'message': 'Email created successfully',
            'email': email.to_dict(include_body=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create email error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create email',
            'message': str(e)
        }), 500


@emails_bp.route('/<int:email_id>', methods=['PUT'])
@jwt_required()
def update_email(email_id):
    """Update an existing email"""
    try:
        user_id = get_jwt_identity()

        # Join with application to verify ownership
        email = Email.query.join(Application).filter(
            Email.id == email_id,
            Application.user_id == user_id
        ).first()

        if not email:
            return jsonify({
                'success': False,
                'error': 'Email not found'
            }), 404

        data = request.get_json()

        # Update fields
        if 'to_email' in data:
            email.to_email = data['to_email'].strip()
        if 'to_name' in data:
            email.to_name = data['to_name']
        if 'subject' in data:
            email.subject = data['subject'].strip()
        if 'body' in data:
            email.body = data['body']
        if 'html_body' in data:
            email.html_body = data['html_body']
        if 'status' in data:
            email.status = data['status']
        if 'priority' in data:
            email.priority = data['priority']
        if 'scheduled_time' in data:
            email.scheduled_time = data['scheduled_time']
        if 'attachments' in data:
            email.attachments = data['attachments']
        if 'error_message' in data:
            email.error_message = data['error_message']

        email.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Email updated: {email.id}')

        return jsonify({
            'success': True,
            'message': 'Email updated successfully',
            'email': email.to_dict(include_body=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update email error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update email',
            'message': str(e)
        }), 500


@emails_bp.route('/<int:email_id>', methods=['DELETE'])
@jwt_required()
def delete_email(email_id):
    """Delete an email"""
    try:
        user_id = get_jwt_identity()

        # Join with application to verify ownership
        email = Email.query.join(Application).filter(
            Email.id == email_id,
            Application.user_id == user_id
        ).first()

        if not email:
            return jsonify({
                'success': False,
                'error': 'Email not found'
            }), 404

        db.session.delete(email)
        db.session.commit()

        current_app.logger.info(f'Email deleted: {email_id}')

        return jsonify({
            'success': True,
            'message': 'Email deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete email error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete email',
            'message': str(e)
        }), 500


# Email Batch Routes

@emails_bp.route('/batches', methods=['GET'])
@jwt_required()
def get_email_batches():
    """Get list of email batches for the current user"""
    try:
        user_id = get_jwt_identity()

        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)

        # Filter parameters
        status = request.args.get('status')

        # Build query
        query = EmailBatch.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        # Order by created date (newest first)
        query = query.order_by(EmailBatch.created_at.desc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        include_emails = request.args.get('include_emails', 'false').lower() == 'true'

        return jsonify({
            'success': True,
            'batches': [batch.to_dict(include_emails=include_emails) for batch in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get email batches error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve email batches',
            'message': str(e)
        }), 500


@emails_bp.route('/batches/<int:batch_id>', methods=['GET'])
@jwt_required()
def get_email_batch(batch_id):
    """Get a single email batch by ID"""
    try:
        user_id = get_jwt_identity()
        batch = EmailBatch.query.filter_by(id=batch_id, user_id=user_id).first()

        if not batch:
            return jsonify({
                'success': False,
                'error': 'Email batch not found'
            }), 404

        include_emails = request.args.get('include_emails', 'true').lower() == 'true'

        return jsonify({
            'success': True,
            'batch': batch.to_dict(include_emails=include_emails)
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get email batch error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve email batch',
            'message': str(e)
        }), 500


@emails_bp.route('/batches', methods=['POST'])
@jwt_required()
def create_email_batch():
    """Create a new email batch"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Create batch
        batch = EmailBatch(
            user_id=user_id,
            name=data.get('name', f'Batch {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}'),
            description=data.get('description'),
            status=data.get('status', EmailBatch.STATUS_DRAFT)
        )

        db.session.add(batch)
        db.session.commit()

        current_app.logger.info(f'Email batch created: {batch.id} for user {user_id}')

        return jsonify({
            'success': True,
            'message': 'Email batch created successfully',
            'batch': batch.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create email batch error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create email batch',
            'message': str(e)
        }), 500


@emails_bp.route('/batches/<int:batch_id>', methods=['PUT'])
@jwt_required()
def update_email_batch(batch_id):
    """Update an existing email batch"""
    try:
        user_id = get_jwt_identity()
        batch = EmailBatch.query.filter_by(id=batch_id, user_id=user_id).first()

        if not batch:
            return jsonify({
                'success': False,
                'error': 'Email batch not found'
            }), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            batch.name = data['name']
        if 'description' in data:
            batch.description = data['description']
        if 'status' in data:
            batch.status = data['status']

        db.session.commit()

        current_app.logger.info(f'Email batch updated: {batch.id}')

        return jsonify({
            'success': True,
            'message': 'Email batch updated successfully',
            'batch': batch.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update email batch error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update email batch',
            'message': str(e)
        }), 500


@emails_bp.route('/batches/<int:batch_id>', methods=['DELETE'])
@jwt_required()
def delete_email_batch(batch_id):
    """Delete an email batch"""
    try:
        user_id = get_jwt_identity()
        batch = EmailBatch.query.filter_by(id=batch_id, user_id=user_id).first()

        if not batch:
            return jsonify({
                'success': False,
                'error': 'Email batch not found'
            }), 404

        db.session.delete(batch)
        db.session.commit()

        current_app.logger.info(f'Email batch deleted: {batch_id}')

        return jsonify({
            'success': True,
            'message': 'Email batch deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete email batch error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete email batch',
            'message': str(e)
        }), 500
