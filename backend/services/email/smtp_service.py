"""
SMTP Email Service for PhD Application Automator
Handles email sending via SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import Config
import logging
from typing import List, Optional
import os

logger = logging.getLogger(__name__)


class SMTPEmailService:
    """Service for sending emails via SMTP"""

    def __init__(self):
        """Initialize SMTP service with configuration"""
        self.smtp_host = Config.MAIL_SERVER
        self.smtp_port = Config.MAIL_PORT
        self.use_tls = Config.MAIL_USE_TLS
        self.username = Config.MAIL_USERNAME
        self.password = Config.MAIL_PASSWORD
        self.from_email = Config.MAIL_DEFAULT_SENDER
        self.from_name = Config.MAIL_DEFAULT_SENDER_NAME

        if not self.username or not self.password:
            logger.warning("SMTP credentials not configured")

        logger.info("SMTP email service initialized")

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: List[str] = None,
        is_html: bool = True
    ) -> bool:
        """
        Send email via SMTP

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            attachments: List of file paths to attach
            is_html: Whether body is HTML

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            attachment = MIMEApplication(f.read())
                            attachment.add_header(
                                'Content-Disposition',
                                'attachment',
                                filename=os.path.basename(file_path)
                            )
                            msg.attach(attachment)

            # Connect and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                if self.use_tls:
                    server.starttls()

                if self.username and self.password:
                    server.login(self.username, self.password)

                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def test_connection(self) -> bool:
        """Test SMTP connection"""
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                if self.use_tls:
                    server.starttls()

                if self.username and self.password:
                    server.login(self.username, self.password)

            logger.info("SMTP connection test successful")
            return True

        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False


# Global instance
_smtp_service = None


def get_smtp_service() -> SMTPEmailService:
    """Get or create SMTP service instance"""
    global _smtp_service
    if _smtp_service is None:
        _smtp_service = SMTPEmailService()
    return _smtp_service
