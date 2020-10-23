"""
# coding:utf-8
@Time    : 2020/10/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : soul_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.sql.expression import func

from blogin.models import Soul, Blog, SongCi
from blogin.utils import Lunar
import datetime

soul_bp = Blueprint('soul_bp', __name__)


@soul_bp.route('/soul/')
def index():
    soul = Soul.query.order_by(func.random()).limit(1)
    return render_template("main/soul.html", soul=soul)


@soul_bp.route('/api/get_soul/')
def get_soul():
    counts = request.args.get('counts', 1)
    if counts == 'all':
        souls = Soul.query.all()
    else:
        souls = Soul.query.order_by(func.random()).limit(int(counts))
    result = {'result': [], 'code': 200}
    for soul in souls:
        ls = {'title': soul.title, 'hits': soul.hits}
        result.get('result').append(ls)
    return jsonify(result)


@soul_bp.route('/api/introduce/')
def api_introduce():
    blog = Blog.query.filter_by(title='API介绍').first()
    return render_template("main/api/apiIntroduce.html", blog=blog)


@soul_bp.route('/song-ci/')
def song_ci():
    ci = SongCi.query.order_by(func.random()).limit(1)[0]
    now = datetime.date.today()
    lundar = Lunar(datetime.datetime.now())
    return render_template('main/poem/songCi.html', ci=ci, now=now, lundar=lundar)
