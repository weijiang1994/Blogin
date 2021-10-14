"""
# coding:utf-8
@Time    : 2021/03/12
@Author  : jiangwei
@File    : msg_border.py
@Desc    : msg_border
@Software: PyCharm
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from blogin.models import MessageBorder
from blogin.extension import db
from bs4 import BeautifulSoup
from blogin.blueprint.front.tool import to_html

msg_border_bp = Blueprint('msg_border_bp', __name__, url_prefix='/msg-border')


@msg_border_bp.route('/')
def index():
    msg_borders = MessageBorder.query.filter(MessageBorder.flag == 0, MessageBorder.parent_id == 0). \
        order_by(MessageBorder.timestamps.desc()).all()
    return render_template('main/message-border.html', msg_borders=msg_borders)


@msg_border_bp.route('/leave-msg/', methods=['POST'])
@login_required
def leave_msg():
    message = request.form.get('message')
    body = to_html(message)
    bse = BeautifulSoup(body, 'html.parser')
    mb = MessageBorder(user_id=current_user.id, body=body, plain_text=bse.get_text())
    db.session.add(mb)
    db.session.commit()
    return '留言成功!'


@msg_border_bp.route('/operator/<msg_id>/')
@login_required
def operator(msg_id):
    msg = MessageBorder.query.get_or_404(msg_id)
    if msg.flag:
        msg.flag = 0
        flash('显示留言成功!', 'success')
    else:
        msg.flag = 1
        flash('屏蔽留言成功!', 'success')
    db.session.commit()
    return redirect(url_for('.index'))
