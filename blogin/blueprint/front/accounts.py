"""
# coding:utf-8
@Time    : 2020/9/24
@Author  : jiangwei
@File    : accounts
@Software: PyCharm
"""
from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user, logout_user
from imageio import imread

from blogin.decorators import db_exception_handle, confirm_required
from blogin.extension import db
from blogin.forms.auth import ChangePwdForm, EditProfileForm
from blogin.setting import basedir
from blogin.models import User, LoginLog, BlogComment, PhotoComment, Notification

accounts_bp = Blueprint('accounts_bp', __name__, url_prefix='/accounts')


@accounts_bp.route('/profile')
@login_required
def profile():
    user_id = current_user.id
    blog_comments = BlogComment.query.filter_by(author_id=user_id).order_by(BlogComment.timestamp.desc()).all()
    photo_comments = PhotoComment.query.filter_by(author_id=user_id).order_by(PhotoComment.timestamp.desc()).all()
    notifies = Notification.query.filter_by(receive_id=current_user.id, read=0). \
        order_by(Notification.timestamp.desc()).all()
    return render_template('main/profile/account-profile.html',
                           blogComments=blog_comments,
                           photoComments=photo_comments)


@accounts_bp.route('/notifications')
@login_required
def notifications():
    notifies = Notification.query.filter_by(receive_id=current_user.id, read=0). \
        order_by(Notification.timestamp.desc()).all()
    return render_template('main/profile/notifications.html', notifies=notifies)


@accounts_bp.route('/login-record')
@login_required
def login_record():
    page = request.args.get('page', 1, type=int)
    pagination = LoginLog.query.filter_by(user_id=current_user.id).order_by(LoginLog.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['LOGIN_LOG_PER_PAGE'])
    logs = pagination.items
    notifies = Notification.query.filter_by(receive_id=current_user.id, read=0). \
        order_by(Notification.timestamp.desc()).all()
    return render_template('main/profile/login-record.html', logs=logs, notifies=notifies, pagination=pagination)


@accounts_bp.route('/password/change/', methods=['GET', 'POST'])
@login_required
@confirm_required
@db_exception_handle(db)
def change_password():
    form = ChangePwdForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.set_password(form.confirm_pwd.data)
        db.session.commit()
        flash('密码修改成功,请重新登录.', 'success')
        logout_user()
        return redirect(url_for('auth_bp.login'))
    return render_template('main/profile/change-password.html', form=form)


@accounts_bp.route('/profile/edit/', methods=['GET', 'POST'])
@login_required
@confirm_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        new_name = form.user_name.data
        user.website = form.website.data
        user.slogan = form.slogan.data
        user.received_email_tag = form.receive_email.data
        query_name_user = User.query.filter_by(username=new_name).first()
        if query_name_user is not None and query_name_user.id != current_user.id:
            flash('用户名已存在', 'danger')
            return render_template('main/profile/edit-profile.html', form=form)
        user.username = form.user_name.data
        if form.avatar.data.filename:
            filename = form.avatar.data.filename
            filename = str(current_user.username) + filename
            form.avatar.data.save(basedir + '/uploads/avatars/' + filename)
            img_data = imread(basedir + '/uploads/avatars/' + filename)
            if len(img_data) != len(img_data[0]):
                flash('为了头像显示正常，请上传长宽一致的头像!', 'danger')
                return render_template('main/profile/edit-profile.html', form=form)
            user.avatar = '/accounts/avatar/' + filename
        db.session.commit()
        flash('资料修改成功!', 'success')
        return redirect(url_for('.profile', user_id=current_user.id))
    form.slogan.data = current_user.slogan
    form.website.data = current_user.website
    form.user_name.data = current_user.username
    form.receive_email.data = current_user.received_email_tag
    return render_template('main/profile/edit-profile.html', form=form)


@accounts_bp.route('/avatar/<filename>/')
def get_avatar(filename):
    path = basedir + '/uploads/avatars/'
    return send_from_directory(path, filename)


@accounts_bp.route('/mark/<int:notify_id>/')
@login_required
def mark_notify(notify_id):
    no = Notification.query.get_or_404(notify_id)
    no.read = 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(url_for('.profile', user_id=current_user.id))


@accounts_bp.route('/mark-all/')
@login_required
def mark_all():
    notifies = Notification.query.filter_by(receive_id=current_user.id).all()
    for notify in notifies:
        notify.read = 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(url_for('.profile', user_id=current_user.id))
