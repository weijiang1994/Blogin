"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : user_manage_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template
from blogin.models import User

user_m_bp = Blueprint('user_m_bp', __name__, url_prefix='/backend')


@user_m_bp.route('/user-m/index/')
def index():
    users = User.query.all()
    return render_template('backend/userManager.html', users=users)
