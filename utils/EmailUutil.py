from flask import render_template
from flask_mail import Mail, Message

from enumeration.EmailTemplateEnum import EmailTemplateEnum
from utils.config import params

mail = Mail()

def init_email(app):
    mail.init_app(app)

def send_email(subject, body, email_list):
    msg = Message(subject, sender=params['MAIL_USERNAME'], recipients=email_list, body=body)
    mail.send(msg)

def send_htm_email(template: EmailTemplateEnum, email_list, **kwargs):
    subject = template.value.get('subject')
    msg = Message(subject, sender=params['MAIL_USERNAME'], recipients=email_list)
    msg.html = render_template(template.value.get('file_path'), **kwargs)
    mail.send(msg)
