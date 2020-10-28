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

from blogin.models import Soul, SongCi, Poem
from blogin.utils import Lunar
import datetime

soul_bp = Blueprint('soul_bp', __name__)


@soul_bp.route('/soul/')
def index():
    soul = Soul.query.order_by(func.random()).limit(1)
    return render_template("main/soul.html", soul=soul)


@soul_bp.route('/song-ci/')
def song_ci():
    ci = SongCi.query.order_by(func.random()).limit(1)[0]
    now = datetime.date.today()
    lundar = Lunar(datetime.datetime.now())
    return render_template('main/poem/songCi.html', ci=ci, now=now, lundar=lundar)


@soul_bp.route('/ts-poem/')
def ts_poem():
    poem = Poem.query.order_by(func.random()).limit(1)[0]
    now = datetime.date.today()
    lundar = Lunar(datetime.datetime.now())
    return render_template('main/poem/tsPoem.html', poem=poem, now=now, lundar=lundar)
