"""
coding:utf-8
file: responses.py
@time: 2024/9/17 0:29
@desc:
"""
from flask import jsonify


class R:

    @staticmethod
    def success(code=200, msg='success', **kwargs):
        return jsonify({
            'code': code,
            'msg': msg,
            **kwargs
        })

    @staticmethod
    def error(code=400, msg='bad request', **kwargs):
        return jsonify({
            'code': code,
            'msg': msg,
            **kwargs
        })

    @staticmethod
    def access_denied():
        return R.error(401, 'access denied')

    @staticmethod
    def not_found():
        return R.error(404, 'not found')

    @staticmethod
    def server_error():
        return R.error(500, 'server error')
