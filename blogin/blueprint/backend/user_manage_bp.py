"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : user_manage_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from blogin.models import User
from blogin.extension import db

user_m_bp = Blueprint('user_m_bp', __name__, url_prefix='/backend/user-m')


@user_m_bp.route('/index/')
def index():
    page = request.args.get('page')
    pagination = User.query.order_by(User.create_time).paginate(page=page,
                                                                per_page=current_app.config['LOGIN_LOG_PER_PAGE'])
    users = pagination.items
    return render_template('backend/userManager.html', pagination=pagination, users=users)


@user_m_bp.route('/set-admin/<int:user_id>/')
def set_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.role_id = 1
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/set-user/<int:user_id>/')
def set_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.email == '804022023@qq.com':
        flash('该账号是超级号，禁止操作!', 'danger')
        return redirect(url_for('.index'))
    user.role_id = 2
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/lock/<int:user_id>/')
def lock(user_id):
    user = User.query.get_or_404(user_id)
    if user.email == '804022023@qq.com':
        flash('该账号是超级号，禁止操作!', 'danger')
        return redirect(url_for('.index'))
    user.status = 2
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))


@user_m_bp.route('/unlock/<int:user_id>/')
def unlock(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 1
    db.session.commit()
    flash('操作成功~', 'success')
    return redirect(url_for('.index'))
