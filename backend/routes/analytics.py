"""
Analytics Routes
Analytics and metrics endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, date
from sqlalchemy import func

from models import db, Analytics, Application, Email, Professor, University


analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/', methods=['GET'])
@jwt_required()
def get_analytics():
    """Get analytics records for the current user"""
    try:
        user_id = get_jwt_identity()

        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        per_page = min(per_page, 100)

        # Filter parameters
        category = request.args.get('category')
        metric_name = request.args.get('metric_name')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Build query
        query = Analytics.query.filter_by(user_id=user_id)

        if category:
            query = query.filter_by(category=category)

        if metric_name:
            query = query.filter_by(metric_name=metric_name)

        if start_date:
            query = query.filter(Analytics.date >= start_date)

        if end_date:
            query = query.filter(Analytics.date <= end_date)

        # Order by date (newest first)
        query = query.order_by(Analytics.date.desc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'success': True,
            'analytics': [metric.to_dict() for metric in pagination.items],
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
        current_app.logger.error(f'Get analytics error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve analytics',
            'message': str(e)
        }), 500


@analytics_bp.route('/<int:analytics_id>', methods=['GET'])
@jwt_required()
def get_analytic(analytics_id):
    """Get a single analytics record by ID"""
    try:
        user_id = get_jwt_identity()
        analytic = Analytics.query.filter_by(id=analytics_id, user_id=user_id).first()

        if not analytic:
            return jsonify({
                'success': False,
                'error': 'Analytics record not found'
            }), 404

        return jsonify({
            'success': True,
            'analytic': analytic.to_dict()
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get analytic error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve analytic',
            'message': str(e)
        }), 500


@analytics_bp.route('/', methods=['POST'])
@jwt_required()
def create_analytic():
    """Create a new analytics record"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Create analytic
        analytic = Analytics(
            user_id=user_id,
            metric_name=data.get('metric_name'),
            metric_value=data.get('metric_value', 0),
            metric_unit=data.get('metric_unit'),
            category=data.get('category'),
            subcategory=data.get('subcategory'),
            date=data.get('date', date.today()),
            hour=data.get('hour'),
            metadata=data.get('metadata', {}),
            dimensions=data.get('dimensions', {})
        )

        db.session.add(analytic)
        db.session.commit()

        current_app.logger.info(f'Analytics record created: {analytic.id}')

        return jsonify({
            'success': True,
            'message': 'Analytics record created successfully',
            'analytic': analytic.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Create analytic error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create analytics record',
            'message': str(e)
        }), 500


@analytics_bp.route('/<int:analytics_id>', methods=['PUT'])
@jwt_required()
def update_analytic(analytics_id):
    """Update an existing analytics record"""
    try:
        user_id = get_jwt_identity()
        analytic = Analytics.query.filter_by(id=analytics_id, user_id=user_id).first()

        if not analytic:
            return jsonify({
                'success': False,
                'error': 'Analytics record not found'
            }), 404

        data = request.get_json()

        # Update fields
        if 'metric_name' in data:
            analytic.metric_name = data['metric_name']
        if 'metric_value' in data:
            analytic.metric_value = data['metric_value']
        if 'metric_unit' in data:
            analytic.metric_unit = data['metric_unit']
        if 'category' in data:
            analytic.category = data['category']
        if 'subcategory' in data:
            analytic.subcategory = data['subcategory']
        if 'metadata' in data:
            analytic.metadata = data['metadata']
        if 'dimensions' in data:
            analytic.dimensions = data['dimensions']

        db.session.commit()

        current_app.logger.info(f'Analytics record updated: {analytics_id}')

        return jsonify({
            'success': True,
            'message': 'Analytics record updated successfully',
            'analytic': analytic.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update analytic error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update analytics record',
            'message': str(e)
        }), 500


@analytics_bp.route('/<int:analytics_id>', methods=['DELETE'])
@jwt_required()
def delete_analytic(analytics_id):
    """Delete an analytics record"""
    try:
        user_id = get_jwt_identity()
        analytic = Analytics.query.filter_by(id=analytics_id, user_id=user_id).first()

        if not analytic:
            return jsonify({
                'success': False,
                'error': 'Analytics record not found'
            }), 404

        db.session.delete(analytic)
        db.session.commit()

        current_app.logger.info(f'Analytics record deleted: {analytics_id}')

        return jsonify({
            'success': True,
            'message': 'Analytics record deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete analytic error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete analytics record',
            'message': str(e)
        }), 500


# Dashboard and Summary Routes

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get dashboard summary statistics"""
    try:
        user_id = get_jwt_identity()

        # Application statistics
        total_applications = Application.query.filter_by(user_id=user_id).count()
        applications_by_status = db.session.query(
            Application.status,
            func.count(Application.id)
        ).filter_by(user_id=user_id).group_by(Application.status).all()

        # Email statistics
        total_emails = Email.query.join(Application).filter(
            Application.user_id == user_id
        ).count()

        emails_by_status = db.session.query(
            Email.status,
            func.count(Email.id)
        ).join(Application).filter(
            Application.user_id == user_id
        ).group_by(Email.status).all()

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_applications = Application.query.filter(
            Application.user_id == user_id,
            Application.created_at >= thirty_days_ago
        ).count()

        recent_emails = Email.query.join(Application).filter(
            Application.user_id == user_id,
            Email.created_at >= thirty_days_ago
        ).count()

        # Response statistics
        replied_count = Application.query.filter(
            Application.user_id == user_id,
            Application.status == Application.STATUS_REPLIED
        ).count()

        interview_count = Application.query.filter(
            Application.user_id == user_id,
            Application.status == Application.STATUS_INTERVIEW
        ).count()

        offer_count = Application.query.filter(
            Application.user_id == user_id,
            Application.status == Application.STATUS_OFFER
        ).count()

        # Response rate
        sent_count = Application.query.filter(
            Application.user_id == user_id,
            Application.status.in_([
                Application.STATUS_SENT,
                Application.STATUS_DELIVERED,
                Application.STATUS_OPENED,
                Application.STATUS_REPLIED,
                Application.STATUS_REJECTED,
                Application.STATUS_INTERVIEW,
                Application.STATUS_OFFER
            ])
        ).count()

        response_rate = (replied_count / sent_count * 100) if sent_count > 0 else 0

        return jsonify({
            'success': True,
            'dashboard': {
                'applications': {
                    'total': total_applications,
                    'by_status': dict(applications_by_status),
                    'recent_30_days': recent_applications,
                    'replied': replied_count,
                    'interviews': interview_count,
                    'offers': offer_count,
                    'response_rate': round(response_rate, 2)
                },
                'emails': {
                    'total': total_emails,
                    'by_status': dict(emails_by_status),
                    'recent_30_days': recent_emails
                }
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get dashboard error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve dashboard data',
            'message': str(e)
        }), 500


@analytics_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    """Get trends data over time"""
    try:
        user_id = get_jwt_identity()

        # Get date range from query params or default to last 30 days
        days = request.args.get('days', 30, type=int)
        days = min(days, 365)  # Max 1 year

        start_date = datetime.utcnow() - timedelta(days=days)

        # Applications per day
        applications_trend = db.session.query(
            func.date(Application.created_at).label('date'),
            func.count(Application.id).label('count')
        ).filter(
            Application.user_id == user_id,
            Application.created_at >= start_date
        ).group_by(func.date(Application.created_at)).all()

        # Emails per day
        emails_trend = db.session.query(
            func.date(Email.created_at).label('date'),
            func.count(Email.id).label('count')
        ).join(Application).filter(
            Application.user_id == user_id,
            Email.created_at >= start_date
        ).group_by(func.date(Email.created_at)).all()

        return jsonify({
            'success': True,
            'trends': {
                'applications': [
                    {'date': str(item.date), 'count': item.count}
                    for item in applications_trend
                ],
                'emails': [
                    {'date': str(item.date), 'count': item.count}
                    for item in emails_trend
                ]
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f'Get trends error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve trends data',
            'message': str(e)
        }), 500
