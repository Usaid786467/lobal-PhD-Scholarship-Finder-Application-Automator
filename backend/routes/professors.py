"""
Professor Routes
CRUD operations for professors
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, Professor, University
from services.utils.validators import validate_required_fields


professors_bp = Blueprint('professors', __name__)


@professors_bp.route('/', methods=['GET'])
@jwt_required()
def get_professors():
    """Get list of professors with pagination and filtering"""
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        per_page = min(per_page, 100)  # Max 100 items per page

        # Filter parameters
        university_id = request.args.get('university_id', type=int)
        accepting_students = request.args.get('accepting_students')
        search = request.args.get('search')

        # Build query
        query = Professor.query

        if university_id:
            query = query.filter_by(university_id=university_id)

        if accepting_students is not None:
            accepting_bool = accepting_students.lower() == 'true'
            query = query.filter_by(accepting_students=accepting_bool)

        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    Professor.name.ilike(search_pattern),
                    Professor.department.ilike(search_pattern),
                    Professor.email.ilike(search_pattern)
                )
            )

        # Order by name
        query = query.order_by(Professor.name.asc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'success': True,
            'professors': [prof.to_dict() for prof in pagination.items],
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
        current_app.logger.error(f'Get professors error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve professors',
            'message': str(e)
        }), 500


@professors_bp.route('/<int:professor_id>', methods=['GET'])
@jwt_required()
def get_professor(professor_id):
    """Get a single professor by ID"""
    try:
        professor = Professor.query.get(professor_id)

        if not professor:
            return jsonify({
                'success': False,
                'error': 'Professor not found'
            }), 404

        include_university = request.args.get('include_university', 'false').lower() == 'true'

        return jsonify({
            'success': True,
            'professor': professor.to_dict(include_university=include_university)
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get professor error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve professor',
            'message': str(e)
        }), 500


@professors_bp.route('/', methods=['POST'])
@jwt_required()
def create_professor():
    """Create a new professor"""
    try:
        data = request.get_json()

        # Validate required fields
        is_valid, error = validate_required_fields(data, ['name', 'university_id'])
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400

        # Verify university exists
        university = University.query.get(data['university_id'])
        if not university:
            return jsonify({
                'success': False,
                'error': 'University not found'
            }), 404

        # Create professor
        professor = Professor(
            university_id=data['university_id'],
            name=data['name'].strip(),
            title=data.get('title'),
            email=data.get('email'),
            phone=data.get('phone'),
            department=data.get('department'),
            research_interests=data.get('research_interests', []),
            specializations=data.get('specializations', []),
            h_index=data.get('h_index'),
            citations=data.get('citations'),
            publications_count=data.get('publications_count'),
            publications=data.get('publications', []),
            accepting_students=data.get('accepting_students'),
            current_students_count=data.get('current_students_count'),
            graduated_students_count=data.get('graduated_students_count'),
            profile_url=data.get('profile_url'),
            personal_website=data.get('personal_website'),
            google_scholar_url=data.get('google_scholar_url'),
            research_gate_url=data.get('research_gate_url'),
            linkedin_url=data.get('linkedin_url'),
            lab_name=data.get('lab_name'),
            lab_website=data.get('lab_website'),
            lab_description=data.get('lab_description'),
            active_grants=data.get('active_grants', []),
            total_funding=data.get('total_funding'),
            match_score=data.get('match_score'),
            match_reasons=data.get('match_reasons', []),
            bio=data.get('bio'),
            photo_url=data.get('photo_url'),
            notes=data.get('notes')
        )

        db.session.add(professor)
        db.session.commit()

        current_app.logger.info(f'Professor created: {professor.name}')

        return jsonify({
            'success': True,
            'message': 'Professor created successfully',
            'professor': professor.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create professor error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create professor',
            'message': str(e)
        }), 500


@professors_bp.route('/<int:professor_id>', methods=['PUT'])
@jwt_required()
def update_professor(professor_id):
    """Update an existing professor"""
    try:
        professor = Professor.query.get(professor_id)

        if not professor:
            return jsonify({
                'success': False,
                'error': 'Professor not found'
            }), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            professor.name = data['name'].strip()
        if 'title' in data:
            professor.title = data['title']
        if 'email' in data:
            professor.email = data['email']
        if 'phone' in data:
            professor.phone = data['phone']
        if 'department' in data:
            professor.department = data['department']
        if 'research_interests' in data:
            professor.research_interests = data['research_interests']
        if 'specializations' in data:
            professor.specializations = data['specializations']
        if 'h_index' in data:
            professor.h_index = data['h_index']
        if 'citations' in data:
            professor.citations = data['citations']
        if 'publications_count' in data:
            professor.publications_count = data['publications_count']
        if 'publications' in data:
            professor.publications = data['publications']
        if 'accepting_students' in data:
            professor.accepting_students = data['accepting_students']
        if 'current_students_count' in data:
            professor.current_students_count = data['current_students_count']
        if 'graduated_students_count' in data:
            professor.graduated_students_count = data['graduated_students_count']
        if 'profile_url' in data:
            professor.profile_url = data['profile_url']
        if 'personal_website' in data:
            professor.personal_website = data['personal_website']
        if 'google_scholar_url' in data:
            professor.google_scholar_url = data['google_scholar_url']
        if 'research_gate_url' in data:
            professor.research_gate_url = data['research_gate_url']
        if 'linkedin_url' in data:
            professor.linkedin_url = data['linkedin_url']
        if 'lab_name' in data:
            professor.lab_name = data['lab_name']
        if 'lab_website' in data:
            professor.lab_website = data['lab_website']
        if 'lab_description' in data:
            professor.lab_description = data['lab_description']
        if 'active_grants' in data:
            professor.active_grants = data['active_grants']
        if 'total_funding' in data:
            professor.total_funding = data['total_funding']
        if 'match_score' in data:
            professor.match_score = data['match_score']
        if 'match_reasons' in data:
            professor.match_reasons = data['match_reasons']
        if 'bio' in data:
            professor.bio = data['bio']
        if 'photo_url' in data:
            professor.photo_url = data['photo_url']
        if 'notes' in data:
            professor.notes = data['notes']

        professor.updated_at = datetime.utcnow()
        db.session.commit()

        current_app.logger.info(f'Professor updated: {professor.name}')

        return jsonify({
            'success': True,
            'message': 'Professor updated successfully',
            'professor': professor.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update professor error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update professor',
            'message': str(e)
        }), 500


@professors_bp.route('/<int:professor_id>', methods=['DELETE'])
@jwt_required()
def delete_professor(professor_id):
    """Delete a professor"""
    try:
        professor = Professor.query.get(professor_id)

        if not professor:
            return jsonify({
                'success': False,
                'error': 'Professor not found'
            }), 404

        professor_name = professor.name
        db.session.delete(professor)
        db.session.commit()

        current_app.logger.info(f'Professor deleted: {professor_name}')

        return jsonify({
            'success': True,
            'message': 'Professor deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete professor error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete professor',
            'message': str(e)
        }), 500
