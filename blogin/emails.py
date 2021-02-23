"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : emails
@Software: PyCharm
"""
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from blogin.extension import mail


def _send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to_email, subject, template, **kwargs):
    message = Message(current_app.config['BLOGIN_MAIL_SUBJECT_PRE'] + subject, recipients=[to_email],
                      sender=current_app.config['MAIL_USERNAME'])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    th_send = Thread(target=_send_async_mail, args=(app, message))
    th_send.start()
    return th_send


def send_server_warning_mail(to_email, subject, template, **kwargs):
    message = Message(current_app.config['BLOGIN_MAIL_SUBJECT_PRE'] + subject, recipients=[to_email],
                      sender=current_app.config['MAIL_USERNAME'])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    th_send = Thread(target=_send_async_mail, args=(app, message))
    th_send.start()
    return th_send


def send_confirm_email(user, token, to=None):
    send_mail(subject='Register Confirm', to_email=to or user.email, template='email/confirm', user=user, token=token)


def send_reset_password_email(user, token, ver_code):
    send_mail(subject='Reset Password', to_email=user.email, template='email/verifyCode', token=token,
              ver_code=ver_code, username=user.username)


def send_network_warning_email(blacklist):
    send_mail(subject='WARNING', to_email='804022023@qq.com', template='email/network-warning', blacklist=blacklist)


def send_server_warning_mail(cpu_rate, mem_rate):
    send_mail(subject='WARNING!', to_email='804022023@qq.com', template='email/warning', cpu_rate=cpu_rate,
              mem_rate=mem_rate)
