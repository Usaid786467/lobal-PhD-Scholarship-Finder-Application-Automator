"""
Database CLI Commands
"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from models import db
import shutil
from datetime import datetime


@click.group()
def db_group():
    """Database management commands"""
    pass


@db_group.command('init')
def init_db():
    """Initialize database tables"""
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            click.echo(click.style('✓ Database initialized successfully!', fg='green'))
    except Exception as e:
        click.echo(click.style(f'✗ Error initializing database: {str(e)}', fg='red'))


@db_group.command('migrate')
def migrate_db():
    """Run database migrations"""
    click.echo('Running database migrations...')
    os.system('flask db upgrade')
    click.echo(click.style('✓ Migrations completed!', fg='green'))


@db_group.command('backup')
def backup_db():
    """Backup database"""
    try:
        db_path = 'phd.db'
        if not os.path.exists(db_path):
            click.echo(click.style('✗ Database file not found', fg='red'))
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'phd_backup_{timestamp}.db'

        shutil.copy2(db_path, backup_path)
        click.echo(click.style(f'✓ Database backed up to {backup_path}', fg='green'))
    except Exception as e:
        click.echo(click.style(f'✗ Error backing up database: {str(e)}', fg='red'))


@db_group.command('reset')
@click.confirmation_option(prompt='Are you sure you want to reset the database?')
def reset_db():
    """Reset database (WARNING: deletes all data)"""
    try:
        app = create_app()
        with app.app_context():
            db.drop_all()
            db.create_all()
            click.echo(click.style('✓ Database reset successfully!', fg='green'))
    except Exception as e:
        click.echo(click.style(f'✗ Error resetting database: {str(e)}', fg='red'))


# Export as 'db' command
db = db_group
