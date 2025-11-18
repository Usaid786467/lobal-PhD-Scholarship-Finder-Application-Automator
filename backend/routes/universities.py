"""
University Routes for PhD Application Automator
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_session, University, Professor, User
from sqlalchemy import or_, and_

universities_bp = Blueprint('universities', __name__)


@universities_bp.route('/search', methods=['GET'])
@jwt_required()
def search_universities():
    """Search universities with filters"""
    try:
        user_id = get_jwt_identity()
        session = get_session()

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        country = request.args.get('country')
        has_scholarship = request.args.get('has_scholarship', type=bool)
        search_query = request.args.get('q', '').strip()

        # Build query
        query = session.query(University).filter_by(is_active=True)

        if country:
            query = query.filter_by(country=country)

        if has_scholarship is not None:
            query = query.filter_by(has_scholarship=has_scholarship)

        if search_query:
            query = query.filter(
                or_(
                    University.name.ilike(f'%{search_query}%'),
                    University.city.ilike(f'%{search_query}%')
                )
            )

        # Order by match score if available
        query = query.order_by(University.match_score.desc().nullslast())

        # Paginate
        total = query.count()
        universities = query.offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            'universities': [u.to_dict(include_details=False) for u in universities],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }), 200

    except Exception as e:
        current_app.logger.error(f'University search error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/<int:university_id>', methods=['GET'])
@jwt_required()
def get_university(university_id):
    """Get university details"""
    try:
        session = get_session()
        university = session.query(University).filter_by(id=university_id).first()

        if not university:
            return jsonify({'error': 'University not found'}), 404

        return jsonify({'university': university.to_dict(include_details=True)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/discover', methods=['POST'])
@jwt_required()
def discover_universities():
    """Trigger university discovery (scraping)"""
    try:
        data = request.get_json() or {}
        countries = data.get('countries', [])

        # TODO: Trigger scraping task
        # For now, return placeholder
        return jsonify({
            'message': 'University discovery started',
            'job_id': 'placeholder-job-id',
            'countries': countries
        }), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/<int:university_id>/professors', methods=['GET'])
@jwt_required()
def get_university_professors(university_id):
    """Get professors at a university"""
    try:
        session = get_session()
        professors = session.query(Professor).filter_by(
            university_id=university_id,
            is_active=True
        ).order_by(Professor.match_score.desc().nullslast()).all()

        return jsonify({
            'professors': [p.to_dict(include_details=False) for p in professors],
            'count': len(professors)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
