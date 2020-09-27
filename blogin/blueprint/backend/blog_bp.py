"""
# coding:utf-8
@Time    : 2020/9/22
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : blog_bp
@Software: PyCharm
"""
import os

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, \
    send_from_directory
from flask_ckeditor import upload_fail, upload_success

from blogin import basedir
from blogin.blueprint.backend.forms import PostForm
from blogin.models import BlogType, Blog
from blogin.extension import db
from blogin.utils import get_current_time, create_path
from flask_login import login_required
from blogin.decorators import permission_required, db_exception_handle


be_blog_bp = Blueprint('be_blog_bp', __name__, url_prefix='/backend')


@be_blog_bp.route('/admin/index/')
@login_required
@permission_required
def index():
    return render_template('backend/index.html')


@be_blog_bp.route('/admin/blog/create/', methods=['GET', 'POST'])
def blog_create():
    form = PostForm()
    if request.method == 'GET':
        return render_template('backend/createBlog.html', form=form)

    if form.validate_on_submit():
        # 获取表单中信息
        title = form.title.data
        type = form.blog_type.choices[int(form.blog_type.data) - 1][0]
        level = form.blog_level.data
        content = form.body.data
        introduce = form.brief_content.data
        filename = form.blog_img_file.data.filename

        current_time = get_current_time()
        current_time = current_time.split(' ')[0]
        create_path(basedir + '/uploads/image/' + current_time)
        # 将博客示例图片存储到对应的文件夹中
        form.blog_img_file.data.save(basedir + '/uploads/image/' + current_time + '/' + filename)
        blog_img_path = '/backend/blog/img/' + current_time + '/' + filename

        cate = BlogType.query.filter_by(id=type).first()
        blg = Blog(title=title, type_id=cate.id, introduce=introduce, content=content, pre_img=blog_img_path,
                   is_private=level-1)
        cate.counts += 1
        db.session.add(blg)
        db.session.commit()

        return redirect(url_for('blog_bp.index'))
    else:
        flash('不能提交包含空的表单!', 'danger')
        return render_template('backend/createBlog.html', form=form)


@be_blog_bp.route('/admin/blog/edit/')
def blog_edit():
    blog_type_datas = []
    types = BlogType.query.all()
    blogs = Blog.query.all()
    for _type in types:
        blog_type_datas.append([_type.id, _type.name, _type.create_time, _type.counts, _type.description,
                                '/backend/editArticleType/' + str(_type.id)])
    return render_template('backend/editBlog.html', blog_type_datas=blog_type_datas, blogs=blogs)


@be_blog_bp.route('/blog/delete/<blog_id>', methods=['GET', 'POST'])
def delete(blog_id):
    Blog.query.filter_by(id=blog_id).delete()
    db.session.commit()
    return redirect(url_for('.blog_edit'))


@be_blog_bp.route('/blog/category/add/', methods=['POST'])
@permission_required
@db_exception_handle(db)
def blog_category_add():
    category_name = request.form.get('name')
    desc = request.form.get('desc')
    if BlogType.query.filter_by(name=category_name).first():
        return jsonify({"is_exists": True})
    cate = BlogType(name=category_name, description=desc)
    db.session.add(cate)
    db.session.commit()
    return jsonify({"is_exists": False})


@be_blog_bp.route('/blog/img/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = basedir + '/uploads/image/' + path + '/'
    return send_from_directory(path, filename)


@be_blog_bp.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['BLOGIN_UPLOAD_PATH']
    return send_from_directory(path, filename)


@be_blog_bp.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    import random
    pre = random.randint(1, 10000)
    filename = str(pre) + f.filename
    f.save(os.path.join(current_app.config['BLOGIN_UPLOAD_PATH'], filename))
    url = url_for('be_blog_bp.uploaded_files', filename=filename)
    return upload_success(url=url)
