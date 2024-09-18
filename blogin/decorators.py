"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@File    : decorators
@Software: PyCharm
"""
from datetime import datetime
from datetime import date
from functools import wraps

from flask import Markup, flash, url_for, redirect, abort, request, jsonify
from flask_login import current_user


# 某些操作需要确认后才能进行
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirm:
            message = Markup(
                '请先前往邮箱确认你的账号!'
                '没有收到邮件?'
                '<a class="alert-link" href="%s">重新发送确认邮件</a>' %
                url_for('auth_bp.resend_confirm_mail'))
            flash(message, 'warning')
            return redirect(url_for('blog_bp.index'))
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
            td = date.today()
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


def get_params(
        params: list,
        types: list = [],
        check_para: bool = False,
        remove_none: bool = False,
):
    """
    获取请求中的参数
    :param remove_none: 是否移除值为空的参数
    :param check_para: 是否检查参数完整
    :param params: 参数列表
    :param types: 参数类型
    :return: 参数列表所对应的参数值
    """
    def decorator(func):
        @wraps(func)
        def wrapper():
            kwarg = {}
            if request.method == 'GET':
                if len(types) != len(params):
                    types.append()
                for param, category in zip(params, types):
                    # 对于bool类型的参数特殊处理，因为如果传入的为false也会当做为True
                    if category == bool:
                        if request.args.get(param, default='false').lower() == 'true':
                            kwarg[param] = True
                        else:
                            kwarg[param] = False
                    else:
                        value = request.args.get(param, type=category)
                        kwarg[param] = value
            elif request.method == 'POST':
                for idx, param in enumerate(params):
                    value = request.json.get(param)
                    if value:
                        kwarg[param] = types[idx](value)
                    else:
                        kwarg[param] = None
            if check_para:
                if None in kwarg.values() or '' in kwarg.values():
                    return jsonify(dict(
                        code=403,
                        msg='参数不完整,请检查参数后重试!'
                    ))
            if remove_none:
                kwarg = dict(filter(lambda x: x[1] not in [None, ''], kwarg.items()))

            return func(**kwarg)

        return wrapper

    return decorator
