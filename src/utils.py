from flask_mail import Message
from flask import copy_current_request_context
from threading import Thread

from src.extensions import mail
from src.config import Config


def send_email(subject, text):
    message = Message(subject=subject, html=text, recipients=[Config.MAIL_USERNAME], sender=Config.MAIL_USERNAME)

    @copy_current_request_context
    def send_message(message):
        mail.send(message)

    thread = Thread(target=send_message, args=[message])
    thread.start()
