"""
# coding:utf-8
@Time    : 2020/10/26
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : api
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify, render_template
from blogin.models import Soul, Blog
from sqlalchemy.sql.expression import func

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')


@api_bp.route('/introduce/')
def api_introduce():
    blog = Blog.query.filter_by(title='API介绍').first()
    return render_template("main/api/apiIntroduce.html", blog=blog)


@api_bp.route('/get-soul/')
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
