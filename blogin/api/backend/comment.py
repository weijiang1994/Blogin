"""
coding:utf-8
file: comment.py
@time: 2024/10/6 23:20
@desc:
"""
from flask import Blueprint

from flask_jwt_extended import jwt_required

from blogin.api.decorators import get_params, check_permission
from blogin.models import BlogComment, PhotoComment
from blogin.responses import R

api_comment_bp = Blueprint('api_comment_bp', __name__, url_prefix='/api/comment')


@api_comment_bp.route('/blog/list', methods=['GET'])
@get_params(
    params=['page', 'limit', 'blog_id', 'status', 'user_id', 'content'],
    types=[int, int, int, int, int, str],
    remove_none=True
)
@jwt_required
@check_permission
def blog_comment_list(page, limit=10, blog_id=None, status=None, user_id=None, content=None):
    query = (BlogComment.id > 0,)
    if blog_id:
        query += (BlogComment.blog_id == blog_id,)
    if status is not None:
        query += (BlogComment.delete_flag == status,)
    if user_id:
        query += (BlogComment.author_id == user_id,)
    if content:
        query += (BlogComment.body.contains(content),)
    comments = BlogComment.query.filter(
        *query
    ).order_by(
        BlogComment.timestamp.desc()
    ).paginate(
        per_page=limit,
        page=page
    )
    data = []
    for comment in comments.items:
        item = comment.to_dict()
        item['user'] = comment.author.username
        item['blog'] = comment.blog.title
        item['status'] = '屏蔽' if comment.delete_flag else '正常'

        data.append(item)
    return R.success(
        total=comments.total,
        data=data
    )


@api_comment_bp.route('/photo/list', methods=['GET'])
@get_params(
    params=['page', 'limit', 'photo_id', 'status', 'user_id', 'content'],
    types=[int, int, int, int, int, str],
    remove_none=True
)
@jwt_required
@check_permission
def photo_comment_list(page, limit=10, photo_id=None, status=None, user_id=None, content=None):
    query = (PhotoComment.id > 0,)
    if photo_id:
        query += (PhotoComment.photo_id == photo_id,)
    if status is not None:
        query += (PhotoComment.delete_flag == status,)
    if user_id:
        query += (PhotoComment.author_id == user_id,)
    if content:
        query += (PhotoComment.body.contains(content),)
    comments = PhotoComment.query.filter(
        *query
    ).order_by(
        PhotoComment.timestamp.desc()
    ).paginate(
        per_page=limit,
        page=page
    )
    data = []
    for comment in comments.items:
        item = comment.to_dict()
        item['user'] = comment.author.username
        item['photo'] = comment.photo.title
        item['status'] = '屏蔽' if comment.delete_flag else '正常'

        data.append(item)
    return R.success(
        total=comments.total,
        data=data
    )


@api_comment_bp.route('/delete', methods=['POST'])
@get_params(
    params=['comment_id', 'category'],
    types=[int, str]
)
@jwt_required
@check_permission
def delete_comment(comment_id, category):
    if category == 'blog':
        comment = BlogComment.query.get(comment_id)
    else:
        comment = PhotoComment.query.get(comment_id)
    if not comment:
        return R.error(msg='评论不存在')
    comment.delete_flag = 1
    comment.save()
    return R.success(msg='评论已屏蔽')


@api_comment_bp.route('/recover', methods=['POST'])
@get_params(
    params=['comment_id', 'category'],
    types=[int, str]
)
@jwt_required
@check_permission
def recover_comment(comment_id, category):
    if category == 'blog':
        comment = BlogComment.query.get(comment_id)
    else:
        comment = PhotoComment.query.get(comment_id)
    if not comment:
        return R.error(msg='评论不存在')
    comment.delete_flag = 0
    comment.save()
    return R.success(msg='评论已恢复')
