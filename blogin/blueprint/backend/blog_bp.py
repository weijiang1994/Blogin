"""
# coding:utf-8
@Time    : 2020/9/22
@Author  : jiangwei
@File    : blog_bp
@Software: PyCharm
"""
import os
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, \
    send_from_directory
from flask_ckeditor import upload_fail, upload_success
from blogin import basedir
from blogin.blueprint.backend.forms import PostForm, EditPostForm
from blogin.models import BlogType, Blog, States, BlogHistory, ContributeDetail, DraftBlog, PostContent, \
    update_contribution
from blogin.extension import db
from blogin.utils import get_current_time, create_path, get_md5
from flask_login import login_required
from blogin.decorators import permission_required, db_exception_handle
import datetime

be_blog_bp = Blueprint('be_blog_bp', __name__, url_prefix='/backend')


@be_blog_bp.route('/blog/top/<blog_id>/')
@login_required
@permission_required
def set_top(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.is_top:
        blog.is_top = 0
    else:
        etp = Blog.query.filter_by(is_top=1).first()
        if etp and etp.id != blog.id:
            flash('已经存在了置顶文章,请先取消后再操作!', 'danger')
            return redirect(request.referrer)
        else:
            blog.is_top = 1
    db.session.commit()
    flash('操作成功!', 'success')
    return redirect(request.referrer)


@be_blog_bp.route('/admin/blog/create/', methods=['GET', 'POST'])
@login_required
@permission_required
def blog_create():
    form = PostForm()
    drafts = DraftBlog.query.filter_by(tag=1).all()
    draft_id = request.args.get('draft-id')
    if request.method == 'GET':
        if draft_id:
            c_draft = DraftBlog.query.get_or_404(draft_id)
            form.title.data = c_draft.title
            form.body.data = c_draft.content
            form.brief_content.data = c_draft.brief
        return render_template('backend/create-blog.html', drafts=drafts, form=form, draft_id=draft_id)

    if form.validate_on_submit():
        # 获取表单中信息
        title = form.title.data
        content = form.body.data
        introduce = form.brief_content.data
        filename = form.blog_img_file.data.filename
        _type = form.blog_type.data
        level = form.blog_level.data
        bs = BeautifulSoup(content, 'html.parser')
        catalogue = [link.get('id') for link in bs.find_all('a') if link.get('id')]

        current_time = get_current_time()
        current_time = current_time.split(' ')[0]
        create_path(basedir + '/uploads/image/' + current_time)
        # 将博客示例图片存储到对应的文件夹中
        form.blog_img_file.data.save(basedir + '/uploads/image/' + current_time + '/' + filename)
        blog_img_path = '/backend/blog/img/' + current_time + '/' + filename

        cate = BlogType.query.filter_by(id=_type).first()
        state = States.query.get_or_404(1)
        blg = Blog(title=title, type_id=cate.id, introduce=introduce, content=content, pre_img=blog_img_path,
                   is_private=level - 1, state=state)
        cate.counts += 1
        update_contribution()
        db.session.add(blg)
        db.session.add(PostContent(content=str(catalogue), post_id=blg.id))
        db.session.commit()
        return redirect(url_for('blog_bp.index'))
    else:
        flash('不能提交包含空的表单!', 'danger')
        return render_template('backend/create-blog.html', form=form, drafts=drafts, draft_id=draft_id)


@be_blog_bp.route('/admin/blog/edit/')
@login_required
@permission_required
def blog_edit():
    page = request.args.get('page', 1, type=int)
    blog_type_datas = []
    types = BlogType.query.all()
    pagination = Blog.query.order_by(Blog.create_time).paginate(page=page,
                                                                per_page=20)
    blogs = pagination.items
    for _type in types:
        blog_type_datas.append([_type.id, _type.name, _type.create_time, _type.counts, _type.description,
                                '/backend/edit-article-cate/{}/'.format(str(_type.id))])
    return render_template('backend/edit-blog.html', blog_type_datas=blog_type_datas, blogs=blogs,
                           pagination=pagination)


@be_blog_bp.route('/edit-article-cate/<cate_id>/', methods=['GET', 'POST'])
@login_required
@permission_required
def edit_cate(cate_id):
    cate = BlogType.query.get_or_404(cate_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cate.name = name
        cate.description = description
        db.session.commit()
        flash('编辑类别信息成功!', 'success')
    return render_template('backend/edit-blog-category.html', cate=cate)


@be_blog_bp.route('/blog/edit/<int:blog_id>', methods=['GET', 'POST'])
@login_required
@permission_required
def blog_content_edit(blog_id):
    form = EditPostForm()
    blog = Blog.query.get_or_404(blog_id)
    if form.validate_on_submit():
        history_content = blog.content
        filename = form.blog_img_file.data.filename
        if filename != '':
            blog_img_path = save_blog_img(filename, form)
            blog.pre_img = blog_img_path

        blog.content = form.body.data
        blog.title = form.title.data
        type = form.blog_type.data
        cate = BlogType.query.filter_by(id=type).first()
        blog.type_id = cate.id
        blog.introduce = form.brief_content.data
        blog.update_time = datetime.datetime.now()
        bs = BeautifulSoup(form.body.data, 'html.parser')
        catalogue = [link.get('id') for link in bs.find_all('a') if link.get('id')]
        post_cate = PostContent.query.filter_by(post_id=blog.id).first()
        if post_cate:
            post_cate.content = str(catalogue)
        else:
            db.session.add(PostContent(content=str(catalogue), post_id=blog.id))

        update_contribution()
        history_file_path = basedir + '/history/' + get_md5(get_current_time()) + '.txt'

        if not os.path.exists(basedir + '/history/'):
            os.makedirs(basedir + '/history/')

        with open(history_file_path, 'w', encoding='utf-8') as f:
            f.write(history_content)
        bh = BlogHistory(blog_id=blog.id, save_path=history_file_path, timestamps=datetime.datetime.now())
        db.session.add(bh)
        db.session.commit()

        return redirect(url_for('blog_bp.blog_article', blog_id=blog_id))

    form.title.data = blog.title
    form.blog_type.data = blog.type_id
    form.brief_content.data = blog.introduce
    form.body.data = blog.content
    return render_template('backend/editBlogContent.html', form=form)


def save_blog_img(filename, form):
    current_time = get_current_time()
    current_time = current_time.split(' ')[0]
    create_path(basedir + '/uploads/image/' + current_time)
    # 将博客示例图片存储到对应的文件夹中
    form.blog_img_file.data.save(basedir + '/uploads/image/' + current_time + '/' + filename)
    blog_img_path = '/backend/blog/img/' + current_time + '/' + filename
    return blog_img_path


@be_blog_bp.route('/blog/delete/<blog_id>/', methods=['GET', 'POST'])
@login_required
@permission_required
def delete(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    state = States.query.get_or_404(2)
    blog.state = state
    db.session.commit()
    flash('博客删除成功~', 'success')
    return redirect(url_for('.blog_edit'))


@be_blog_bp.route('/blog/recover/<blog_id>/', methods=['GET', 'POST'])
@login_required
@permission_required
def recover(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    state = States.query.get_or_404(1)
    blog.state = state
    db.session.commit()
    flash('博客恢复成功~', 'success')
    return redirect(url_for('.blog_edit'))


@be_blog_bp.route('/blog/category/add/', methods=['POST'])
@login_required
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
    url = url_for('be_blog_bp.uploaded_files', filename=filename, _external=True)
    return upload_success(url=url)


@be_blog_bp.route('/delete-draft/', methods=['POST'])
@permission_required
def delete_draft():
    did = request.form.get('did')
    d = DraftBlog.query.get_or_404(did)
    d.tag = 0
    db.session.commit()
    return jsonify({'tag': 1, 'info': '删除草稿成功!'})


@be_blog_bp.route('/save-draft/', methods=['POST'])
@permission_required
def save_draft():
    did = request.form.get('did')
    title = request.form.get('title')
    content = request.form.get('content')
    brief = request.form.get('brief')

    if did != 'None':
        d = DraftBlog.query.get_or_404(did)
        d.content = content
        d.title = title
        d.brief = brief
    else:
        d = DraftBlog(title=title, content=content, brief=brief)
        db.session.add(d)
    db.session.commit()
    return jsonify({'tag': 1, 'info': '保存草稿成功', 'draft_id': d.id})
