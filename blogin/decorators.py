# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from datetime import datetime
from functools import wraps

from flask import Markup, flash, url_for, redirect, abort
from flask_login import current_user


# 某些操作需要确认后才能进行
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirm:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_function


# 后台管理页面不允许普通用户登入
def permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.role_id == 1:
            abort(403)
        return func(*args, **kwargs)

    return decorated_function


def db_exception_handle(db):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                import traceback
                traceback.print_exc()
                db.session.rollback()
                abort(500)
        return decorated_function
    return decorator


def statistic_traffic(db, obj):
    """
    网站今日访问量、评论量、点赞量统计装饰器
    :param db: 数据库操作对象
    :param obj: 统计模型类别(VisitStatistics,CommentStatistics,LikeStatistics)
    :return:
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            td = datetime.today().strftime('%Y-%m-%d')
            vst = obj.query.filter_by(date=td).first()
            if vst is None:
                new_vst = obj(date=td, times=1)
                db.session.add(new_vst)
            else:
                vst.times += 1
            db.session.commit()
            return func(*args, **kwargs)
        return decorated_function
    return decorator
