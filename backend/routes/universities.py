"""
Universities Routes
API endpoints for university discovery and management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, University
from services.scraper import UniversityScraper
import json

universities_bp = Blueprint('universities', __name__, url_prefix='/api/universities')


@universities_bp.route('/search', methods=['GET'])
@jwt_required()
def search_universities():
    """
    Search universities with filters
    GET /api/universities/search?country=USA&research=aerospace&has_scholarship=true&page=1&per_page=20
    """
    try:
        # Get query parameters
        country = request.args.get('country')
        research = request.args.get('research')
        has_scholarship = request.args.get('has_scholarship')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = University.query

        if country:
            query = query.filter_by(country=country)

        if has_scholarship == 'true':
            query = query.filter_by(has_scholarship=True)

        if research:
            # Search in research_areas JSON field
            query = query.filter(University.research_areas.contains(research))

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'universities': [uni.to_dict() for uni in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/discover', methods=['POST'])
@jwt_required()
def discover_universities():
    """
    Trigger university discovery/scraping
    POST /api/universities/discover
    Body: {country: 'USA', limit: 100}
    """
    try:
        data = request.get_json() or {}
        country = data.get('country')
        limit = data.get('limit', 50)

        # Initialize scraper
        scraper = UniversityScraper()

        # Scrape universities
        universities_data = scraper.scrape_universities(country=country, limit=limit)

        # Save to database
        saved_count = 0
        for uni_data in universities_data:
            # Check if exists
            existing = University.query.filter_by(
                name=uni_data['name'],
                country=uni_data['country']
            ).first()

            if existing:
                # Update existing
                for key, value in uni_data.items():
                    setattr(existing, key, value)
            else:
                # Create new
                university = University(**uni_data)
                db.session.add(university)

            saved_count += 1

        db.session.commit()

        return jsonify({
            'message': f'Successfully discovered {saved_count} universities',
            'count': saved_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/<int:university_id>', methods=['GET'])
@jwt_required()
def get_university(university_id):
    """Get university by ID"""
    try:
        university = University.query.get(university_id)
        if not university:
            return jsonify({'error': 'University not found'}), 404

        return jsonify(university.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/countries', methods=['GET'])
@jwt_required()
def get_countries():
    """Get list of available countries"""
    try:
        scraper = UniversityScraper()
        countries = scraper.get_available_countries()

        # Also get countries from database
        db_countries = db.session.query(University.country).distinct().all()
        db_countries = [c[0] for c in db_countries]

        # Combine and deduplicate
        all_countries = list(set(countries + db_countries))
        all_countries.sort()

        return jsonify({'countries': all_countries}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@universities_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get university statistics"""
    try:
        total = University.query.count()
        by_country = db.session.query(
            University.country,
            db.func.count(University.id)
        ).group_by(University.country).all()

        with_scholarships = University.query.filter_by(has_scholarship=True).count()

        return jsonify({
            'total': total,
            'by_country': {country: count for country, count in by_country},
            'with_scholarships': with_scholarships
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
