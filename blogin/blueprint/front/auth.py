"""
# coding:utf-8
@Time    : 2020/9/24
@Author  : jiangwei
@File    : auth
@Software: PyCharm
"""
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from blogin.forms.forms import ResetPwdForm

from blogin.forms.auth import RegisterForm, LoginForm
from blogin.models import User, LoginLog
from blogin.extension import db
from blogin.utils import get_ip_real_add, generate_token, Operations, validate_token, generate_ver_code
from blogin.emails import send_confirm_email, send_reset_password_email
from blogin.extension import rd

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.user_name.data
        pwd = form.confirm_pwd.data
        email = form.user_email.data.lower()
        user = User(username=name, email=email, password=pwd, )
        user.set_password(pwd)
        user.set_role()
        db.session.add(user)
        db.session.commit()
        token = generate_token(user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('注册成功,欢迎加入Blogin.', 'success')
        return redirect(url_for('.login'))
    return render_template('main/auth/register.html', form=form)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # 若当前已有用户登录则返回主页
    if current_user.is_authenticated:
        return redirect(url_for('blog_bp.index'))

    remote_ip = request.headers.get('X-Real-Ip')
    if remote_ip is None:
        remote_ip = request.remote_addr
    ban_ip = rd.get(str(remote_ip))

    form = LoginForm()
    if ban_ip is not None:
        if int(ban_ip) >= 5:
            flash('当前IP登录错误次数过多,已被禁止登录,请明天再试!', 'info')
            return render_template('main/auth/login.html', form=form)

    if form.validate_on_submit():
        usr = form.usr_email.data
        pwd = form.password.data
        user = User.query.filter(or_(User.username == usr, User.email == usr.lower())).first()
        if user is not None and user.status == 2:
            flash('您的账号处于封禁状态,禁止登陆！联系管理员解除封禁!', 'danger')
            return redirect(url_for('.login'))

        if user is not None and user.check_password(pwd):
            if login_user(user, form.remember_me.data):
                user.recent_login = datetime.now()
                login_log = LoginLog(login_addr=remote_ip, user=user, real_addr=get_ip_real_add(remote_ip))
                db.session.add(login_log)
                db.session.commit()
                flash('登录成功!', 'success')
                if request.args.get('next'):
                    return redirect(url_for(request.args.next))
                print(request.referrer)
                return redirect(request.referrer)
        elif user is None:
            flash('无效的邮箱或用户名.', 'danger')
        else:
            if ban_ip is None:
                rd.set(str(request.remote_addr), str(1), ex=60*60*24)
            else:
                rd.set(str(request.remote_addr), str(int(ban_ip)+1), ex=60*60*24)
            flash('无效的密码', 'danger')
    return render_template('main/auth/login.html', form=form)


@auth_bp.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('退出成功!', 'success')
    return redirect(url_for('blog_bp.index'))


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if validate_token(user=current_user, operation=Operations.CONFIRM, token=token):
        flash('邮箱确认成功!', 'success')
    else:
        flash('不是你的就别想有拥有啦!╭(╯^╰)╮  邮箱验证失败啦!', 'danger')
    return redirect(url_for('blog_bp.index'))


@auth_bp.route('/forget-password/')
def forget_pwd():
    return render_template('main/auth/forget-pwd.html')


@auth_bp.route('/password-reset/', methods=['GET', 'POST'])
def reset_password():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('邮箱不存在,请输入正确的邮箱!', 'danger')
        return redirect(url_for('.forget_pwd'))
    ver_code = generate_ver_code()
    # 将验证码设置到redis中,过期时间为10分钟
    rd.set(user.id, ver_code, ex=current_app.config['EXPIRE_TIME'])
    token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
    send_reset_password_email(user=user, token=token, ver_code=ver_code)
    flash('验证邮件发送成功，请到邮箱查看然后重置密码!', 'success')
    return render_template('main/auth/pwd-reset-next.html')


@auth_bp.route('/reset-confirm/', methods=['POST', 'GET'])
def reset_confirm():
    if current_user.is_authenticated:
        return redirect(url_for('.login'))

    form = ResetPwdForm()
    if form.validate_on_submit():
        email = form.email.data
        usr = User.query.filter_by(email=email).first()
        # 如果输入的邮箱不存在
        if not usr:
            flash('邮箱不存在，请输入正确的邮箱~', 'danger')
            return render_template('main/auth/reset-pwd.html', form=form)
        # 如果验证码已经超出了有效时间
        if rd.get(usr.id) is None:
            flash('验证码已过期.', 'danger')
            return render_template('main/auth/reset-pwd.html', form=form)
        pwd = form.confirm_pwd.data
        ver_code = form.ver_code.data

        # 如果输入的验证码与redis中的不一致
        if ver_code != rd.get(usr.id):
            flash('验证码错误')
            return render_template('main/auth/reset-pwd.html', form=form)
        usr.set_password(pwd)
        db.session.commit()
        flash('密码重置成功!', 'success')
        return redirect(url_for('.login'))
    return render_template('main/auth/reset-pwd.html', form=form)


@auth_bp.route('/resend-confirm/')
@login_required
def resend_confirm_mail():
    user = current_user._get_current_object()
    token = generate_token(user=user, operation=Operations.CONFIRM)
    send_confirm_email(user=user, token=token)
    flash('邮箱认证邮件发送成功，请前往邮箱查看认证!', 'success')
    return redirect(request.referrer)
