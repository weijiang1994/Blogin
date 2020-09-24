"""
# coding:utf-8
@Time    : 2020/9/24
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : gallery
@Software: PyCharm
"""
from flask import Blueprint
from blogin.models import Photo
from blogin.models import PhotoComment

gallery_bp = Blueprint('gallery_bp', __name__, url_prefix='/gallery')


@gallery_bp.route('/all/', methods=['GET', 'POST'])
def all():
    pass