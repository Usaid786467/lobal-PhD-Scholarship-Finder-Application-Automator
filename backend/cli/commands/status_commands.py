"""
Status CLI Commands
"""
import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from models import db, University, Professor, Application, Email, User


@click.command()
def status():
    """Show system status and statistics"""
    try:
        app = create_app()
        with app.app_context():
            # Get counts
            users_count = User.query.count()
            universities_count = University.query.count()
            professors_count = Professor.query.count()
            applications_count = Application.query.count()
            emails_count = Email.query.count()

            # Application stats
            draft_apps = Application.query.filter_by(status='draft').count()
            sent_apps = Application.query.filter_by(status='sent').count()
            replied_apps = Application.query.filter_by(status='replied').count()

            # Email stats
            sent_emails = Email.query.filter_by(status='sent').count()

            click.echo('\n' + '=' * 60)
            click.echo('PhD APPLICATION AUTOMATION SYSTEM - STATUS')
            click.echo('=' * 60)
            click.echo('\nDATABASE STATISTICS:')
            click.echo(f'  Users:                {users_count}')
            click.echo(f'  Universities:         {universities_count}')
            click.echo(f'  Professors:           {professors_count}')
            click.echo(f'  Applications:         {applications_count}')
            click.echo(f'  Emails:               {emails_count}')
            click.echo('\nAPPLICATION STATUS:')
            click.echo(f'  Draft:                {draft_apps}')
            click.echo(f'  Sent:                 {sent_apps}')
            click.echo(f'  Replied:              {replied_apps}')
            click.echo('\nEMAIL STATUS:')
            click.echo(f'  Sent:                 {sent_emails}')

            if sent_apps > 0:
                response_rate = (replied_apps / sent_apps) * 100
                click.echo(f'  Response Rate:        {response_rate:.1f}%')

            click.echo('=' * 60 + '\n')

    except Exception as e:
        click.echo(click.style(f'✗ Error getting status: {str(e)}', fg='red'))
