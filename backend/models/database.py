"""
Database initialization and session management
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Define naming convention for constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    return db


def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        db.create_all()


def drop_tables(app):
    """Drop all database tables"""
    with app.app_context():
        db.drop_all()


def reset_db(app):
    """Reset database (drop and recreate all tables)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
