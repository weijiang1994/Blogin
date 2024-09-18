"""
coding:utf-8
file: __init__.py
@time: 2024/9/17 0:32
@desc:
"""
from flask import Flask

from .frontend.auth import api_auth_bp
from .frontend.index import index_bp


def register_restful_api(app: Flask):
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(index_bp)
