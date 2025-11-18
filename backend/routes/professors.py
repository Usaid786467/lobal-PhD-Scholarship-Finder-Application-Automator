"""
Professors Routes
API endpoints for professor discovery and management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Professor, University, User
from services.scraper import ProfessorScraper
from services.ai import GeminiService, MatchingEngine
from config import Config
import json

professors_bp = Blueprint('professors', __name__, url_prefix='/api/professors')


@professors_bp.route('/search', methods=['GET'])
@jwt_required()
def search_professors():
    """
    Search professors with filters
    GET /api/professors/search?university_id=1&department=Engineering&accepting=true&page=1
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        # Get query parameters
        university_id = request.args.get('university_id', type=int)
        department = request.args.get('department')
        accepting = request.args.get('accepting')
        min_match_score = request.args.get('min_match_score', type=float)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = Professor.query

        if university_id:
            query = query.filter_by(university_id=university_id)

        if department:
            query = query.filter(Professor.department.contains(department))

        if accepting == 'true':
            query = query.filter_by(accepting_students=True)

        # Get professors
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        professors = [prof.to_dict() for prof in pagination.items]

        # Calculate match scores if user has research interests
        if user and user.research_interests:
            gemini = GeminiService(Config.GEMINI_API_KEY)
            matcher = MatchingEngine(gemini)

            for prof in professors:
                score = matcher.calculate_match_score(
                    user.research_interests,
                    prof.get('research_interests', '[]')
                )
                prof['match_score'] = score

            # Filter by minimum match score if specified
            if min_match_score:
                professors = [p for p in professors if p.get('match_score', 0) >= min_match_score]

            # Sort by match score
            professors.sort(key=lambda x: x.get('match_score', 0), reverse=True)

        return jsonify({
            'professors': professors,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@professors_bp.route('/discover', methods=['POST'])
@jwt_required()
def discover_professors():
    """
    Trigger professor discovery/scraping
    POST /api/professors/discover
    Body: {university_id: 1, limit: 50}
    """
    try:
        data = request.get_json() or {}
        university_id = data.get('university_id')
        limit = data.get('limit', 50)

        if not university_id:
            return jsonify({'error': 'university_id is required'}), 400

        university = University.query.get(university_id)
        if not university:
            return jsonify({'error': 'University not found'}), 404

        # Initialize scraper
        scraper = ProfessorScraper()

        # Scrape professors
        professors_data = scraper.scrape_professors(
            university_id=university_id,
            university_name=university.name,
            limit=limit
        )

        # Save to database
        saved_count = 0
        for prof_data in professors_data:
            # Check if exists
            existing = Professor.query.filter_by(
                university_id=university_id,
                email=prof_data['email']
            ).first()

            if existing:
                # Update existing
                for key, value in prof_data.items():
                    setattr(existing, key, value)
            else:
                # Create new
                professor = Professor(**prof_data)
                db.session.add(professor)

            saved_count += 1

        db.session.commit()

        return jsonify({
            'message': f'Successfully discovered {saved_count} professors',
            'count': saved_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@professors_bp.route('/<int:professor_id>', methods=['GET'])
@jwt_required()
def get_professor(professor_id):
    """Get professor by ID"""
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({'error': 'Professor not found'}), 404

        return jsonify(professor.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@professors_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get professor statistics"""
    try:
        total = Professor.query.count()
        accepting = Professor.query.filter_by(accepting_students=True).count()
        by_department = db.session.query(
            Professor.department,
            db.func.count(Professor.id)
        ).group_by(Professor.department).all()

        return jsonify({
            'total': total,
            'accepting_students': accepting,
            'by_department': {dept: count for dept, count in by_department if dept}
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
