"""
# coding:utf-8
@Time    : 2020/9/24
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : accounts
@Software: PyCharm
"""
from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.datastructures import CombinedMultiDict

from blogin.decorators import db_exception_handle
from blogin.extension import db
from blogin.forms.auth import ChangePwdForm, EditProfileForm
from blogin.setting import basedir
from blogin.models import User

accounts_bp = Blueprint('accounts_bp', __name__, url_prefix='/accounts')


@accounts_bp.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    return render_template('main/accountProfile.html')


@accounts_bp.route('/password/change/', methods=['GET', 'POST'])
@login_required
@db_exception_handle(db)
def change_password():
    form = ChangePwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.set_password(form.confirm_pwd.data)
        db.session.commit()
        flash('密码修改成功,请重新登录.', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('main/changePassword.html', form=form)


@accounts_bp.route('/profile/edit/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.website = form.website.data
        user.slogan = form.slogan.data
        if form.avatar.data.filename:
            filename = form.avatar.data.filename
            filename = str(current_user.username) + filename
            form.avatar.data.save(basedir + '/uploads/avatars/'+filename)
            user.avatar = '/accounts/avatar/' + filename
        db.session.commit()
        flash('资料修改成功!', 'success')
        return redirect(url_for('.profile', user_id=current_user.id))
    form.slogan.data = current_user.slogan
    form.website.data = current_user.website
    return render_template('main/editProfile.html', form=form)


@accounts_bp.route('/avatar/<filename>/')
def get_avatar(filename):
    path = basedir + '/uploads/avatars/'
    return send_from_directory(path, filename)
