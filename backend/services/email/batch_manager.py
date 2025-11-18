"""
Batch Manager
Manages batch email operations and tracking
"""
from datetime import datetime
import logging
from typing import List, Dict, Optional
from models import db, Email, EmailBatch, Application

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchManager:
    """Manages email batches and bulk operations"""

    def __init__(self, max_batch_size: int = 50):
        """
        Initialize batch manager
        Args:
            max_batch_size: Maximum emails per batch
        """
        self.max_batch_size = max_batch_size

    def create_batch(self, user_id: int, emails: List[Dict]) -> Optional[EmailBatch]:
        """
        Create new email batch
        Args:
            user_id: User ID
            emails: List of email dictionaries with application_id, subject, body
        Returns:
            Created EmailBatch or None on failure
        """
        try:
            # Create batch
            batch = EmailBatch(
                user_id=user_id,
                total_count=len(emails),
                sent_count=0,
                status='draft'
            )
            db.session.add(batch)
            db.session.flush()  # Get batch ID

            # Create email records
            for email_data in emails:
                email = Email(
                    application_id=email_data['application_id'],
                    batch_id=batch.id,
                    subject=email_data['subject'],
                    body=email_data['body'],
                    status='draft'
                )
                db.session.add(email)

            db.session.commit()
            logger.info(f"Created batch {batch.id} with {len(emails)} emails")
            return batch

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating batch: {str(e)}")
            return None

    def get_batch(self, batch_id: int) -> Optional[EmailBatch]:
        """Get batch by ID"""
        return EmailBatch.query.get(batch_id)

    def get_batch_emails(self, batch_id: int, status: Optional[str] = None) -> List[Email]:
        """
        Get emails in batch
        Args:
            batch_id: Batch ID
            status: Filter by status (optional)
        Returns:
            List of Email objects
        """
        query = Email.query.filter_by(batch_id=batch_id)

        if status:
            query = query.filter_by(status=status)

        return query.all()

    def approve_batch(self, batch_id: int) -> bool:
        """
        Approve batch for sending
        Args:
            batch_id: Batch ID
        Returns:
            True if approved successfully
        """
        try:
            batch = self.get_batch(batch_id)
            if not batch:
                logger.error(f"Batch {batch_id} not found")
                return False

            if batch.status != 'draft':
                logger.error(f"Batch {batch_id} is not in draft status")
                return False

            # Update batch status
            batch.status = 'approved'

            # Update email status
            emails = self.get_batch_emails(batch_id, status='draft')
            for email in emails:
                email.status = 'approved'

            db.session.commit()
            logger.info(f"Batch {batch_id} approved with {len(emails)} emails")
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error approving batch {batch_id}: {str(e)}")
            return False

    def mark_email_sent(self, email_id: int) -> bool:
        """
        Mark email as sent
        Args:
            email_id: Email ID
        Returns:
            True if updated successfully
        """
        try:
            email = Email.query.get(email_id)
            if not email:
                return False

            email.status = 'sent'
            email.sent_at = datetime.utcnow()

            # Update application status
            if email.application:
                email.application.status = 'sent'
                email.application.applied_date = datetime.utcnow()

            # Update batch count
            if email.batch:
                email.batch.sent_count += 1

                # Check if batch complete
                if email.batch.sent_count >= email.batch.total_count:
                    email.batch.status = 'completed'

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking email {email_id} as sent: {str(e)}")
            return False

    def mark_email_failed(self, email_id: int, error_message: str) -> bool:
        """
        Mark email as failed
        Args:
            email_id: Email ID
            error_message: Error message
        Returns:
            True if updated successfully
        """
        try:
            email = Email.query.get(email_id)
            if not email:
                return False

            email.status = 'failed'
            email.error_message = error_message
            email.retry_count += 1

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking email {email_id} as failed: {str(e)}")
            return False

    def get_user_batches(self, user_id: int, limit: int = 10) -> List[EmailBatch]:
        """
        Get user's email batches
        Args:
            user_id: User ID
            limit: Maximum number of batches to return
        Returns:
            List of EmailBatch objects
        """
        return EmailBatch.query.filter_by(user_id=user_id)\
            .order_by(EmailBatch.created_at.desc())\
            .limit(limit)\
            .all()
