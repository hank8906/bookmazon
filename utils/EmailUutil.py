from flask_mail import Mail, Message

from utils.config import params

mail = Mail()


def init_email(app):
    mail.init_app(app)


def send_email(subject, body, email_list):
    msg = Message(subject, sender=params['MAIL_USERNAME'], recipients=email_list, body=body)
    mail.send(msg)
