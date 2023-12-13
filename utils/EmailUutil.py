from flask_mail import Mail, Message

from utils.dev_config import Config

mail = Mail()


def init_email(app):
    mail.init_app(app)


def send_reset_email(token):
    subject = "Password Reset Request"
    body = f"Click the following link to reset your password: http://127.0.0.1:5001/reset_password?token={token}"

    msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[Config.RECEIVE_MAIL_USERNAME], body=body)
    mail.send(msg)
