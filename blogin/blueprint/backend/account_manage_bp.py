"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : user_manage_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from blogin.models import User, BlogComment, PhotoComment
from blogin.extension import db

user_m_bp = Blueprint('user_m_bp', __name__, url_prefix='/backend/interactive')


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


@user_m_bp.route('/blog-comment/')
def blog_comment():
    page = request.args.get('page', default=1, type=int)
    pagination = BlogComment.query.order_by(BlogComment.timestamp).paginate(page=page,
                                                                            per_page=current_app.config[
                                                                                'LOGIN_LOG_PER_PAGE'])
    comments = pagination.items
    return render_template('backend/blog_comments.html', comments=comments, pagination=pagination)


@user_m_bp.route('/lock/blog-comment/<int:com_id>')
def unlock_or_lock_blog_comment(com_id):
    blog_com = BlogComment.query.get_or_404(com_id)
    if blog_com is not None and blog_com.delete_flag == 1:
        blog_com.delete_flag = 0
    else:
        blog_com.delete_flag = 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(url_for('.blog_comment'))
