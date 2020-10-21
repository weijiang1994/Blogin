"""
# coding:utf-8
@Time    : 2020/10/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : soul_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template
from sqlalchemy.sql.expression import func

from blogin.models import Soul
soul_bp = Blueprint('soul_bp', __name__)


@soul_bp.route('/soul/')
def index():
    soul = Soul.query.order_by(func.random()).limit(1)
    print(soul)
    return render_template("main/soul.html", soul=soul)


