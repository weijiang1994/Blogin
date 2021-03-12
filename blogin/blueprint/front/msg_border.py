"""
# coding:utf-8
@Time    : 2021/03/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : msg_border.py
@Desc    : msg_border
@Software: PyCharm
"""
from flask import Blueprint, render_template


msg_border_bp = Blueprint('msg_border_bp', __name__, url_prefix='/msg_border/')


@msg_border_bp.route('/')
def index():
    return render_template('main/message-border.html')
