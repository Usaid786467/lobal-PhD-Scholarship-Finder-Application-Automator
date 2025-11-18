"""
Professor Routes for PhD Application Automator
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_session, Professor, University
from sqlalchemy import or_

professors_bp = Blueprint('professors', __name__)


@professors_bp.route('/search', methods=['GET'])
@jwt_required()
def search_professors():
    """Search professors with filters"""
    try:
        session = get_session()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        university_id = request.args.get('university_id', type=int)
        accepting_students = request.args.get('accepting_students', type=bool)
        search_query = request.args.get('q', '').strip()

        query = session.query(Professor).filter_by(is_active=True)

        if university_id:
            query = query.filter_by(university_id=university_id)

        if accepting_students is not None:
            query = query.filter_by(accepting_students=accepting_students)

        if search_query:
            query = query.filter(
                or_(
                    Professor.name.ilike(f'%{search_query}%'),
                    Professor.department.ilike(f'%{search_query}%')
                )
            )

        query = query.order_by(Professor.match_score.desc().nullslast())

        total = query.count()
        professors = query.offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            'professors': [p.to_dict(include_details=False) for p in professors],
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        current_app.logger.error(f'Professor search error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@professors_bp.route('/<int:professor_id>', methods=['GET'])
@jwt_required()
def get_professor(professor_id):
    """Get professor details"""
    try:
        session = get_session()
        professor = session.query(Professor).filter_by(id=professor_id).first()

        if not professor:
            return jsonify({'error': 'Professor not found'}), 404

        return jsonify({'professor': professor.to_dict(include_details=True)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@professors_bp.route('/<int:professor_id>/notes', methods=['PUT'])
@jwt_required()
def update_professor_notes(professor_id):
    """Update notes for a professor"""
    try:
        data = request.get_json()
        notes = data.get('notes', '')

        session = get_session()
        professor = session.query(Professor).filter_by(id=professor_id).first()

        if not professor:
            return jsonify({'error': 'Professor not found'}), 404

        professor.notes = notes
        session.commit()

        return jsonify({'message': 'Notes updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
