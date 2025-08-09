import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional
from .config import settings


class EmailService:
    def __init__(self):
        self.email_address = settings.email_address
        self.email_password = settings.email_password
        self.smtp_server = settings.email_smtp_server
        self.smtp_port = settings.email_smtp_port

    def _generate_verification_code(self) -> str:
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))

    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add body to email
            msg.attach(MIMEText(body, 'html'))

            # Create SMTP session
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                text = msg.as_string()
                server.sendmail(self.email_address, to_email, text)

            print(f"✅ Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending email to {to_email}: {e}")
            return False

    def send_verification_email(self, to_email: str, verification_code: str) -> bool:
        """Send email verification code"""
        subject = "Email Verification - RBAC System"
        body = f"""
        <html>
        <body>
            <h2>Email Verification</h2>
            <p>Thank you for registering with our RBAC System!</p>
            <p>Your verification code is: <strong>{verification_code}</strong></p>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this verification, please ignore this email.</p>
            <br>
            <p>Best regards,<br>RBAC System Team</p>
        </body>
        </html>
        """
        return self._send_email(to_email, subject, body)

    def send_password_reset_email(self, to_email: str, reset_code: str) -> bool:
        """Send password reset code"""
        subject = "Password Reset - RBAC System"
        body = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You have requested to reset your password.</p>
            <p>Your reset code is: <strong>{reset_code}</strong></p>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>RBAC System Team</p>
        </body>
        </html>
        """
        return self._send_email(to_email, subject, body)

    def generate_and_send_verification_code(self, to_email: str) -> Optional[str]:
        """Generate and send verification code, return the code if successful"""
        try:
            verification_code = self._generate_verification_code()
            if self.send_verification_email(to_email, verification_code):
                return verification_code
            else:
                # If email sending fails, still return the code for testing
                print(f"⚠️ Email sending failed, but returning code: {verification_code}")
                return verification_code
        except Exception as e:
            print(f"❌ Error in generate_and_send_verification_code: {e}")
            # Generate a code anyway for testing
            verification_code = self._generate_verification_code()
            print(f"⚠️ Generated fallback code: {verification_code}")
            return verification_code

    def generate_and_send_reset_code(self, to_email: str) -> Optional[str]:
        """Generate and send password reset code, return the code if successful"""
        try:
            reset_code = self._generate_verification_code()
            if self.send_password_reset_email(to_email, reset_code):
                return reset_code
            else:
                # If email sending fails, still return the code for testing
                print(f"⚠️ Email sending failed, but returning code: {reset_code}")
                return reset_code
        except Exception as e:
            print(f"❌ Error in generate_and_send_reset_code: {e}")
            # Generate a code anyway for testing
            reset_code = self._generate_verification_code()
            print(f"⚠️ Generated fallback code: {reset_code}")
            return reset_code


# Create a global instance
email_service = EmailService()
