"""
Application Routes
CRUD operations for PhD applications
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, Application, Professor, University
from services.utils.validators import validate_required_fields


applications_bp = Blueprint('applications', __name__)


@applications_bp.route('/', methods=['GET'])
@jwt_required()
def get_applications():
    """Get list of applications for the current user with pagination and filtering"""
    try:
        user_id = get_jwt_identity()

        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # Max 100 items per page

        # Filter parameters
        status = request.args.get('status')
        professor_id = request.args.get('professor_id', type=int)
        university_id = request.args.get('university_id', type=int)

        # Build query
        query = Application.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        if professor_id:
            query = query.filter_by(professor_id=professor_id)

        if university_id:
            query = query.filter_by(university_id=university_id)

        # Order by created date (newest first)
        query = query.order_by(Application.created_at.desc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        include_related = request.args.get('include_related', 'false').lower() == 'true'

        return jsonify({
            'success': True,
            'applications': [app.to_dict(include_related=include_related) for app in pagination.items],
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
        current_app.logger.error(f'Get applications error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve applications',
            'message': str(e)
        }), 500


@applications_bp.route('/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    """Get a single application by ID"""
    try:
        user_id = get_jwt_identity()
        application = Application.query.filter_by(id=application_id, user_id=user_id).first()

        if not application:
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404

        include_related = request.args.get('include_related', 'true').lower() == 'true'

        return jsonify({
            'success': True,
            'application': application.to_dict(include_related=include_related)
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get application error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve application',
            'message': str(e)
        }), 500


@applications_bp.route('/', methods=['POST'])
@jwt_required()
def create_application():
    """Create a new application"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['professor_id', 'university_id'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Verify professor and university exist
        professor = Professor.query.get(data['professor_id'])
        if not professor:
            return jsonify({
                'success': False,
                'error': 'Professor not found'
            }), 404

        university = University.query.get(data['university_id'])
        if not university:
            return jsonify({
                'success': False,
                'error': 'University not found'
            }), 404

        # Create application
        application = Application(
            user_id=user_id,
            professor_id=data['professor_id'],
            university_id=data['university_id'],
            status=data.get('status', Application.STATUS_DRAFT),
            priority=data.get('priority', 0),
            match_score=data.get('match_score'),
            match_reasons=data.get('match_reasons', []),
            custom_message=data.get('custom_message'),
            documents=data.get('documents', []),
            cv_version=data.get('cv_version'),
            notes=data.get('notes'),
            tags=data.get('tags', [])
        )

        db.session.add(application)
        db.session.commit()

        current_app.logger.info(f'Application created: {application.id} for user {user_id}')

        return jsonify({
            'success': True,
            'message': 'Application created successfully',
            'application': application.to_dict(include_related=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create application error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create application',
            'message': str(e)
        }), 500


@applications_bp.route('/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_application(application_id):
    """Update an existing application"""
    try:
        user_id = get_jwt_identity()
        application = Application.query.filter_by(id=application_id, user_id=user_id).first()

        if not application:
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404

        data = request.get_json()

        # Update fields
        if 'status' in data:
            application.status = data['status']
        if 'priority' in data:
            application.priority = data['priority']
        if 'match_score' in data:
            application.match_score = data['match_score']
        if 'match_reasons' in data:
            application.match_reasons = data['match_reasons']
        if 'custom_message' in data:
            application.custom_message = data['custom_message']
        if 'documents' in data:
            application.documents = data['documents']
        if 'cv_version' in data:
            application.cv_version = data['cv_version']
        if 'response_content' in data:
            application.response_content = data['response_content']
        if 'response_sentiment' in data:
            application.response_sentiment = data['response_sentiment']
        if 'response_attachments' in data:
            application.response_attachments = data['response_attachments']
        if 'follow_up_date' in data:
            application.follow_up_date = data['follow_up_date']
        if 'follow_up_count' in data:
            application.follow_up_count = data['follow_up_count']
        if 'follow_up_sent' in data:
            application.follow_up_sent = data['follow_up_sent']
        if 'interview_date' in data:
            application.interview_date = data['interview_date']
        if 'decision_date' in data:
            application.decision_date = data['decision_date']
        if 'notes' in data:
            application.notes = data['notes']
        if 'tags' in data:
            application.tags = data['tags']

        application.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Application updated: {application.id}')

        return jsonify({
            'success': True,
            'message': 'Application updated successfully',
            'application': application.to_dict(include_related=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update application error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update application',
            'message': str(e)
        }), 500


@applications_bp.route('/<int:application_id>', methods=['DELETE'])
@jwt_required()
def delete_application(application_id):
    """Delete an application"""
    try:
        user_id = get_jwt_identity()
        application = Application.query.filter_by(id=application_id, user_id=user_id).first()

        if not application:
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404

        db.session.delete(application)
        db.session.commit()

        current_app.logger.info(f'Application deleted: {application_id}')

        return jsonify({
            'success': True,
            'message': 'Application deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete application error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete application',
            'message': str(e)
        }), 500


@applications_bp.route('/<int:application_id>/status', methods=['PATCH'])
@jwt_required()
def update_application_status(application_id):
    """Update application status"""
    try:
        user_id = get_jwt_identity()
        application = Application.query.filter_by(id=application_id, user_id=user_id).first()

        if not application:
            return jsonify({
                'success': False,
                'error': 'Application not found'
            }), 404

        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['status'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        application.update_status(data['status'])

        current_app.logger.info(f'Application status updated: {application_id} to {data["status"]}')

        return jsonify({
            'success': True,
            'message': 'Application status updated successfully',
            'application': application.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update application status error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update application status',
            'message': str(e)
        }), 500
