"""
# coding:utf-8
@Time    : 2021/03/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : msg_border.py
@Desc    : msg_border
@Software: PyCharm
"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from blogin.models import MessageBorder
from blogin.extension import db
from bs4 import BeautifulSoup
from blogin.blueprint.front.tool import to_html

msg_border_bp = Blueprint('msg_border_bp', __name__, url_prefix='/msg_border')


@msg_border_bp.route('/')
def index():
    msg_borders = MessageBorder.query.filter_by(flag=0).order_by(MessageBorder.timestamps.desc()).all()

    return render_template('main/message-border.html', msg_borders=msg_borders)


@msg_border_bp.route('/leave_msg/', methods=['POST'])
@login_required
def leave_msg():
    message = request.form.get('message')
    body = to_html(message)
    bse = BeautifulSoup(body, 'html.parser')
    mb = MessageBorder(user_id=current_user.id, body=body, plain_text=bse.get_text())
    db.session.add(mb)
    db.session.commit()
    return '留言成功!'
