"""
University Routes
CRUD operations for universities
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, University
from services.utils.validators import validate_required_fields


universities_bp = Blueprint('universities', __name__)


@universities_bp.route('/', methods=['GET'])
@jwt_required()
def get_universities():
    """Get list of universities with pagination and filtering"""
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # Max 100 items per page

        # Filter parameters
        country = request.args.get('country')
        has_scholarship = request.args.get('has_scholarship')
        search = request.args.get('search')

        # Build query
        query = University.query

        if country:
            query = query.filter_by(country=country)

        if has_scholarship is not None:
            has_scholarship_bool = has_scholarship.lower() == 'true'
            query = query.filter_by(has_scholarship=has_scholarship_bool)

        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    University.name.ilike(search_pattern),
                    University.city.ilike(search_pattern)
                )
            )

        # Order by name
        query = query.order_by(University.name.asc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'success': True,
            'universities': [uni.to_dict() for uni in pagination.items],
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
        current_app.logger.error(f'Get universities error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve universities',
            'message': str(e)
        }), 500


@universities_bp.route('/<int:university_id>', methods=['GET'])
@jwt_required()
def get_university(university_id):
    """Get a single university by ID"""
    try:
        university = University.query.get(university_id)

        if not university:
            return jsonify({
                'success': False,
                'error': 'University not found'
            }), 404

        include_professors = request.args.get('include_professors', 'false').lower() == 'true'

        return jsonify({
            'success': True,
            'university': university.to_dict(include_professors=include_professors)
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get university error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve university',
            'message': str(e)
        }), 500


@universities_bp.route('/', methods=['POST'])
@jwt_required()
def create_university():
    """Create a new university"""
    try:
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['name', 'country'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Create university
        university = University(
            name=data['name'].strip(),
            country=data['country'].strip(),
            city=data.get('city'),
            state_province=data.get('state_province'),
            website=data.get('website'),
            domain=data.get('domain'),
            contact_email=data.get('contact_email'),
            phone=data.get('phone'),
            address=data.get('address'),
            ranking=data.get('ranking'),
            logo_url=data.get('logo_url'),
            type=data.get('type'),
            research_areas=data.get('research_areas', []),
            departments=data.get('departments', []),
            has_scholarship=data.get('has_scholarship', False),
            scholarship_details=data.get('scholarship_details'),
            scholarship_amount=data.get('scholarship_amount'),
            scholarship_url=data.get('scholarship_url'),
            application_deadline=data.get('application_deadline'),
            application_requirements=data.get('application_requirements', []),
            application_url=data.get('application_url'),
            accepts_international=data.get('accepts_international', True),
            language_requirements=data.get('language_requirements', {}),
            description=data.get('description'),
            notes=data.get('notes')
        )

        db.session.add(university)
        db.session.commit()

        current_app.logger.info(f'University created: {university.name}')

        return jsonify({
            'success': True,
            'message': 'University created successfully',
            'university': university.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create university error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create university',
            'message': str(e)
        }), 500


@universities_bp.route('/<int:university_id>', methods=['PUT'])
@jwt_required()
def update_university(university_id):
    """Update an existing university"""
    try:
        university = University.query.get(university_id)

        if not university:
            return jsonify({
                'success': False,
                'error': 'University not found'
            }), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            university.name = data['name'].strip()
        if 'country' in data:
            university.country = data['country'].strip()
        if 'city' in data:
            university.city = data['city']
        if 'state_province' in data:
            university.state_province = data['state_province']
        if 'website' in data:
            university.website = data['website']
        if 'domain' in data:
            university.domain = data['domain']
        if 'contact_email' in data:
            university.contact_email = data['contact_email']
        if 'phone' in data:
            university.phone = data['phone']
        if 'address' in data:
            university.address = data['address']
        if 'ranking' in data:
            university.ranking = data['ranking']
        if 'logo_url' in data:
            university.logo_url = data['logo_url']
        if 'type' in data:
            university.type = data['type']
        if 'research_areas' in data:
            university.research_areas = data['research_areas']
        if 'departments' in data:
            university.departments = data['departments']
        if 'has_scholarship' in data:
            university.has_scholarship = data['has_scholarship']
        if 'scholarship_details' in data:
            university.scholarship_details = data['scholarship_details']
        if 'scholarship_amount' in data:
            university.scholarship_amount = data['scholarship_amount']
        if 'scholarship_url' in data:
            university.scholarship_url = data['scholarship_url']
        if 'application_deadline' in data:
            university.application_deadline = data['application_deadline']
        if 'application_requirements' in data:
            university.application_requirements = data['application_requirements']
        if 'application_url' in data:
            university.application_url = data['application_url']
        if 'accepts_international' in data:
            university.accepts_international = data['accepts_international']
        if 'language_requirements' in data:
            university.language_requirements = data['language_requirements']
        if 'description' in data:
            university.description = data['description']
        if 'notes' in data:
            university.notes = data['notes']

        university.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'University updated: {university.name}')

        return jsonify({
            'success': True,
            'message': 'University updated successfully',
            'university': university.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update university error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update university',
            'message': str(e)
        }), 500


@universities_bp.route('/<int:university_id>', methods=['DELETE'])
@jwt_required()
def delete_university(university_id):
    """Delete a university"""
    try:
        university = University.query.get(university_id)

        if not university:
            return jsonify({
                'success': False,
                'error': 'University not found'
            }), 404

        university_name = university.name
        db.session.delete(university)
        db.session.commit()

        current_app.logger.info(f'University deleted: {university_name}')

        return jsonify({
            'success': True,
            'message': 'University deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete university error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete university',
            'message': str(e)
        }), 500
