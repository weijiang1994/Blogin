"""
coding:utf-8
file: auth.py
@time: 2024/9/17 0:27
@desc:
"""
from flask import Blueprint, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, current_user
from sqlalchemy import or_
from blogin.extension import jwt
from blogin.models import User
from blogin.responses import R
from blogin.api.decorators import get_params


api_auth_bp = Blueprint('api_auth_bp', __name__, url_prefix='/api/auth')


@api_auth_bp.route('/login', methods=['POST'])
@get_params(
    params=['username', 'password'],
    types=[str, str],
    check_para=True
)
def login(username, password):
    user = User.query.filter(or_(
        User.username == username,
        User.email == username
    )).first()
    if user is None or not user.check_password(password):
        return R.error(401, 'username or password error')

    access_token = create_access_token(identity=user)
    return R.success(data=dict(
        access_token=access_token,
        user=user.to_dict()
    ))


@api_auth_bp.route('/info', methods=['GET'])
@jwt_required
def info():
    user = User.query.get(current_user.id)
    return R.success(data=user.to_dict())


@api_auth_bp.route('/change-password', methods=['POST'])
@jwt_required
@get_params(
    params=['old_password', 'new_password'],
    types=[str, str],
    check_para=True
)
def change_password(old_password, new_password):
    user = User.query.get(current_user.id)
    if not user.check_password(old_password):
        return R.error(401, 'old password error')
    user.set_password(new_password)
    return R.success()


@jwt.user_identity_loader
def user_identity_lookup(user):
    if isinstance(user, int):
        return user
    return user.id


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity) if identity else None


@jwt.unauthorized_loader
def unauthorized_loader_callback(callback):
    return R.error(401, '接口权限校验失败，请登录后重试')


@jwt.expired_token_loader
def expired_token_loader_callback():
    return R.error(401, '登录已过期，请重新登录')
