"""
SMTP Service
Handles email sending via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging
from typing import Optional, List
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMTPService:
    """Service for sending emails via SMTP"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        from_name: str = 'PhD Applicant'
    ):
        """
        Initialize SMTP service
        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_user: SMTP username (email)
            smtp_password: SMTP password
            from_name: Sender name
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_name = from_name

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send email
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            attachments: List of file paths to attach
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.smtp_user}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            attachment = MIMEApplication(f.read())
                            filename = os.path.basename(file_path)
                            attachment.add_header(
                                'Content-Disposition',
                                f'attachment; filename="{filename}"'
                            )
                            msg.attach(attachment)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False

    def test_connection(self) -> bool:
        """
        Test SMTP connection
        Returns:
            True if connection successful
        """
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
            logger.info("SMTP connection test successful")
            return True

        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False

    def send_test_email(self, to_email: str) -> bool:
        """
        Send test email
        Args:
            to_email: Recipient email
        Returns:
            True if sent successfully
        """
        subject = "Test Email - PhD Application System"
        body = """This is a test email from the PhD Application Automation System.

If you received this email, your SMTP configuration is working correctly!

Best regards,
PhD Application System"""

        return self.send_email(to_email, subject, body)
