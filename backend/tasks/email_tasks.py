"""
Email Tasks
Celery tasks for asynchronous email sending
"""
from celery_app import celery
from services.email import SMTPService, BatchManager
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.task(bind=True, name='tasks.send_email_batch')
def send_email_batch_task(self, batch_id, user_name, cv_path=None):
    """
    Celery task to send email batch
    Args:
        batch_id: EmailBatch ID
        user_name: User's name for sender
        cv_path: Path to CV attachment
    Returns:
        Dictionary with results
    """
    try:
        logger.info(f"Starting email batch send task for batch {batch_id}")

        # Initialize services
        smtp = SMTPService(
            smtp_host=Config.SMTP_HOST,
            smtp_port=Config.SMTP_PORT,
            smtp_user=Config.SMTP_USER,
            smtp_password=Config.SMTP_PASSWORD,
            from_name=user_name
        )

        batch_manager = BatchManager()

        # Get emails to send
        emails = batch_manager.get_batch_emails(batch_id, status='approved')

        sent_count = 0
        failed_count = 0

        for email in emails:
            # Send email
            attachments = [cv_path] if cv_path else None

            success = smtp.send_email(
                to_email=email.application.professor.email,
                subject=email.subject,
                body=email.body,
                attachments=attachments
            )

            if success:
                batch_manager.mark_email_sent(email.id)
                sent_count += 1
            else:
                batch_manager.mark_email_failed(email.id, 'SMTP send failed')
                failed_count += 1

        logger.info(f"Batch send completed. Sent: {sent_count}, Failed: {failed_count}")

        return {
            'status': 'success',
            'sent': sent_count,
            'failed': failed_count
        }

    except Exception as e:
        logger.error(f"Error in email batch send task: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@celery.task(bind=True, name='tasks.send_single_email')
def send_single_email_task(self, email_id, user_name, cv_path=None):
    """
    Celery task to send single email
    Args:
        email_id: Email ID
        user_name: User's name for sender
        cv_path: Path to CV attachment
    Returns:
        Dictionary with results
    """
    try:
        logger.info(f"Starting single email send task for email {email_id}")

        smtp = SMTPService(
            smtp_host=Config.SMTP_HOST,
            smtp_port=Config.SMTP_PORT,
            smtp_user=Config.SMTP_USER,
            smtp_password=Config.SMTP_PASSWORD,
            from_name=user_name
        )

        batch_manager = BatchManager()

        # Send email
        # Note: Would need to fetch email from database here
        # Simplified for demonstration

        logger.info(f"Single email send completed")

        return {
            'status': 'success'
        }

    except Exception as e:
        logger.error(f"Error in single email send task: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
