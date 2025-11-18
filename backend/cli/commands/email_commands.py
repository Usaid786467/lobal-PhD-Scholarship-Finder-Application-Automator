"""
Email CLI Commands
"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from models import db, EmailBatch, Email
from services.email import BatchManager


@click.group()
def email_group():
    """Email management commands"""
    pass


@email_group.command('batches')
@click.option('--user-id', '-u', type=int, help='User ID')
@click.option('--limit', '-l', default=10, help='Number of batches to show')
def list_batches(user_id, limit):
    """List email batches"""
    try:
        app = create_app()
        with app.app_context():
            query = EmailBatch.query

            if user_id:
                query = query.filter_by(user_id=user_id)

            batches = query.order_by(EmailBatch.created_at.desc()).limit(limit).all()

            if not batches:
                click.echo('No batches found')
                return

            click.echo('\n' + '=' * 80)
            click.echo(f'{"ID":<10} {"User":<10} {"Total":<10} {"Sent":<10} {"Status":<15} {"Created"}')
            click.echo('=' * 80)

            for batch in batches:
                click.echo(
                    f'{batch.id:<10} '
                    f'{batch.user_id:<10} '
                    f'{batch.total_count:<10} '
                    f'{batch.sent_count:<10} '
                    f'{batch.status:<15} '
                    f'{batch.created_at.strftime("%Y-%m-%d %H:%M")}'
                )

            click.echo('=' * 80 + '\n')

    except Exception as e:
        click.echo(click.style(f'✗ Error listing batches: {str(e)}', fg='red'))


@email_group.command('approve')
@click.option('--batch-id', '-b', required=True, type=int, help='Batch ID')
def approve_batch(batch_id):
    """Approve email batch"""
    try:
        app = create_app()
        with app.app_context():
            batch_manager = BatchManager()
            success = batch_manager.approve_batch(batch_id)

            if success:
                click.echo(click.style(f'✓ Batch {batch_id} approved successfully!', fg='green'))
            else:
                click.echo(click.style(f'✗ Failed to approve batch {batch_id}', fg='red'))

    except Exception as e:
        click.echo(click.style(f'✗ Error approving batch: {str(e)}', fg='red'))


@email_group.command('stats')
def email_stats():
    """Show email statistics"""
    try:
        app = create_app()
        with app.app_context():
            total_batches = EmailBatch.query.count()
            total_emails = Email.query.count()
            sent_emails = Email.query.filter_by(status='sent').count()
            draft_emails = Email.query.filter_by(status='draft').count()

            click.echo('\n' + '=' * 50)
            click.echo('EMAIL STATISTICS')
            click.echo('=' * 50)
            click.echo(f'Total Batches:    {total_batches}')
            click.echo(f'Total Emails:     {total_emails}')
            click.echo(f'Sent Emails:      {sent_emails}')
            click.echo(f'Draft Emails:     {draft_emails}')
            click.echo('=' * 50 + '\n')

    except Exception as e:
        click.echo(click.style(f'✗ Error getting stats: {str(e)}', fg='red'))


# Export as 'email' command
email = email_group
