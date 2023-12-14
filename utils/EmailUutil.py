from flask_mail import Mail, Message

from utils.dev_config import Config

mail = Mail()


def init_email(app):
    mail.init_app(app)

def send_email(token,subject,body):
    msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[Config.RECEIVE_MAIL_USERNAME], body=body)
    mail.send(msg)
