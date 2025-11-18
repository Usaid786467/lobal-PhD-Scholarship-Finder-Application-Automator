"""
Email Services Package
SMTP and batch email management
"""
from .smtp_service import SMTPService
from .batch_manager import BatchManager
from .scheduler import EmailScheduler

__all__ = ['SMTPService', 'BatchManager', 'EmailScheduler']
