from flask import render_template, jsonify, abort, make_response
from flask_mail import Message

from __project_name__.extensions import mail


def send_mail(sender: str, to: str, subject: str, template: str, **kwargs):

    msg = Message(sender=sender,
                  recipients=[to],
                  subject=subject,
                  html=render_template(template, **kwargs))

    try:
        mail.send(msg)
    except Exception as exc:
        abort(make_response(
            jsonify({'errors': f'Mail server. {str(exc)}'}), 500))
