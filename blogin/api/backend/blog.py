"""
coding:utf-8
file: blog.py
@time: 2024/9/22 23:32
@desc:
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from blogin.models import Blog, BlogType, States, BlogComment
from blogin.responses import R
from blogin.api.decorators import check_permission, get_params
from blogin.utils import config_ini

blog_bp = Blueprint('blog_backend_bp', __name__, url_prefix='/api/blog')


@blog_bp.errorhandler(404)
def page_not_found(e):
    return R.not_found()


@blog_bp.route('/list', methods=['GET'])
@get_params(
    params=['page', 'status', 'title', 'category'],
    types=[int, int, str, int],
)
@jwt_required
@check_permission
def blog_list(page, status=0, title='', category=0):
    query = (Blog.id > 0,)

    if status:
        query += (Blog.delete_flag == status,)

    if title:
        query += (Blog.title.contains(title),)

    if category:
        query += (Blog.type_id == category,)

    blogs = Blog.query.order_by(
        Blog.create_time.desc()
    ).filter(
        *query
    ).paginate(
        per_page=10,
        page=page,
    )

    data = []
    for blog in blogs.items:
        item = blog.to_dict(
            special_col={
                'pre_img': lambda x: config_ini.get('server', 'host') + x,
                'is_private': lambda x: '私密' if x else '公开',
            },
        )
        item['type'] = blog.blog_types.name
        item['comment_times'] = len(blog.comments)
        item['status'] = blog.state.name
        data.append(item)

    return R.success(
        data=data,
        has_next=blogs.has_next,
        has_prev=blogs.has_prev,
        page=page,
        total=blogs.total,
    )


@blog_bp.route('/delete/<blog_id>', methods=['POST'])
@jwt_required
@check_permission
def delete(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    state = States.query.get_or_404(2)
    blog.state = state
    db.session.commit()
    return R.success(msg='博客删除成功')


@blog_bp.route('/recover/<blog_id>', methods=['POST'])
@jwt_required
@check_permission
def recover(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    state = States.query.get_or_404(1)
    blog.state = state
    db.session.commit()
    return R.success(msg='博客恢复成功')


@blog_bp.route('/category/add', methods=['POST'])
@get_params(
    params=['name', 'description'],
    types=[str, str]
)
@jwt_required
@check_permission
def blog_category_add(name, description):
    if BlogType.query.filter_by(name=name).first():
        return R.error(msg='分类已存在')
    cate = BlogType(name=name, description=description)
    cate.save()
    return R.success(msg='博客分类添加成功')


@blog_bp.route('/category/list', methods=['GET'])
@jwt_required
@check_permission
def blog_category_list():
    categories = BlogType.query.order_by(BlogType.create_time.desc()).all()
    data = []
    for category in categories:
        data.append(category.to_dict())
    return R.success(data=data)
