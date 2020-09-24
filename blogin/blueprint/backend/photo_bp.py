"""
# coding:utf-8
@Time    : 2020/9/23
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : photo_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template
from blogin.blueprint.backend.forms import AddPhotoForm


be_photo_bp = Blueprint('be_photo_bp', __name__, url_prefix='/backend')


@be_photo_bp.route('/photo/add/', methods=['GET', 'POST'])
def add_photo():
    form = AddPhotoForm()
    if form.validate_on_submit():

        pass
    return render_template('backend/addPhoto.html', form=form)
