from flask_mail import Message
from app import mail
from flask import current_app

def send_email(to, subject, body):
    msg = Message(
        subject,
        recipients=[to],
        body=body,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Email failed: {e}")
        return False
