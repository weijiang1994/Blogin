"""
coding:utf-8
file: user.py
@time: 2024/10/7 10:14
@desc:
"""
from flask import Blueprint

from flask_jwt_extended import jwt_required

from blogin.api.decorators import get_params, check_permission
from blogin.models import User
from blogin.responses import R


api_user_bp = Blueprint('api_user_bp', __name__, url_prefix='/api/user')


@api_user_bp.route('/list', methods=['GET'])
@get_params(
    params=['page', 'limit', 'username', 'email', 'status'],
    types=[int, int, str, str, int],
    remove_none=True
)
@jwt_required
@check_permission
def user_list(page=1, limit=10, username=None, email=None, status=None):
    query = (User.id > 0,)
    if username:
        query += (User.username.contains(username),)
    if email:
        query += (User.email.contains(email),)
    if status is not None:
        query += (User.status == status,)

    users = User.query.filter(
        *query
    ).order_by(
        User.create_time.desc()
    ).paginate(
        per_page=limit,
        page=page
    )

    data = []
    for user in users.items:
        item = user.to_dict()
        item['status'] = '正常' if user.status == 1 else '禁用'
        data.append(item)
    return R.success(
        total=users.total,
        data=data
    )
