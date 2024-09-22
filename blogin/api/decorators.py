"""
coding:utf-8
file: decorators.py
@time: 2024/9/22 23:36
@desc:
"""
from functools import wraps

from flask_jwt_extended import current_user
from flask import request

from blogin.models import Blog, User
from blogin.responses import R


def check_permission(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role == 1:
            return func(*args, **kwargs)
        return R.access_denied()

    return wrapper


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
