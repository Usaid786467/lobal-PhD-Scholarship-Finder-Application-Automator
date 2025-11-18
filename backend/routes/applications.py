"""
Applications Routes
API endpoints for application tracking
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Application, Professor

applications_bp = Blueprint('applications', __name__, url_prefix='/api/applications')


@applications_bp.route('/', methods=['GET'])
@jwt_required()
def get_applications():
    """
    Get user's applications with filters
    GET /api/applications?status=sent&page=1&per_page=20
    """
    try:
        user_id = get_jwt_identity()

        # Get query parameters
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Build query
        query = Application.query.filter_by(user_id=user_id)

        if status:
            query = query.filter_by(status=status)

        # Paginate
        pagination = query.order_by(Application.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'applications': [app.to_dict() for app in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    """Get application by ID"""
    try:
        user_id = get_jwt_identity()
        application = Application.query.get(application_id)

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        if application.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify(application.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_application(application_id):
    """
    Update application
    PUT /api/applications/<id>
    Body: {status: 'replied', notes: 'Professor responded positively'}
    """
    try:
        user_id = get_jwt_identity()
        application = Application.query.get(application_id)

        if not application:
            return jsonify({'error': 'Application not found'}), 404

        if application.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json() or {}

        if 'status' in data:
            application.status = data['status']
        if 'notes' in data:
            application.notes = data['notes']

        db.session.commit()

        return jsonify({
            'message': 'Application updated successfully',
            'application': application.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@applications_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get application statistics"""
    try:
        user_id = get_jwt_identity()

        total = Application.query.filter_by(user_id=user_id).count()
        by_status = db.session.query(
            Application.status,
            db.func.count(Application.id)
        ).filter_by(user_id=user_id).group_by(Application.status).all()

        return jsonify({
            'total': total,
            'by_status': {status: count for status, count in by_status}
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
