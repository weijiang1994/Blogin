"""
# coding:utf-8
@Time    : 2020/9/22
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : blog_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, request, jsonify
from blogin.blueprint.backend.forms import PostForm
from blogin.models import BlogType
from blogin.extension import db


be_blog_bp = Blueprint('be_blog_bp', __name__, url_prefix='/backend')


@be_blog_bp.route('/admin/index/')
def index():
    return render_template('backend/index.html')


@be_blog_bp.route('/admin/blog/create/')
def blog_create():
    form = PostForm()
    return render_template('backend/createBlog.html', form=form)


@be_blog_bp.route('/admin/blog/edit/')
def blog_edit():
    blog_type_datas = []
    types = BlogType.query.all()
    print(types)
    for _type in types:
        blog_type_datas.append([_type.id, _type.name, _type.create_time, _type.counts, _type.description,
                                '/backend/editArticleType/' + _type.id])
    return render_template('backend/editBlog.html', blog_type_datas=blog_type_datas)


@be_blog_bp.route('/blog/category/add/', methods=['POST'])
def blog_category_add():
    category_name = request.form.get('name')
    desc = request.form.get('desc')
    if BlogType.query.filter_by(name=category_name).first():
        return jsonify({"is_exists": True})
    cate = BlogType(name=category_name, description=desc)
    db.session.add(cate)
    db.session.commit()

    return jsonify({"is_exists": False})
