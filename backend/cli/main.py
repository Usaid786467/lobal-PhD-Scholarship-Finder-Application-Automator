#!/usr/bin/env python3
"""
PhD Automator CLI
Command-line interface for the PhD Application Automation System
"""
import click
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commands import db_commands, scrape_commands, email_commands, status_commands


@click.group()
@click.version_option('1.0.0')
def cli():
    """PhD Application Automation System CLI"""
    pass


# Register command groups
cli.add_command(db_commands.db)
cli.add_command(scrape_commands.scrape)
cli.add_command(email_commands.email)
cli.add_command(status_commands.status)


if __name__ == '__main__':
    cli()
