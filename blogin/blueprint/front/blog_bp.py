"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : blog_bp
@Software: PyCharm
"""
from flask import Blueprint, render_template, flash, redirect, url_for, request
from blogin.models import Blog, BlogType, LoveMe, LoveInfo
from blogin.extension import db
from flask_login import current_user

blog_bp = Blueprint('blog_bp', __name__)


@blog_bp.route('/', methods=['GET'])
@blog_bp.route('/index/', methods=['GET'])
def index():
    blogs = Blog.query.order_by(Blog.create_time.desc()).all()
    cates = []
    for blog in blogs:
        cates.append(BlogType.query.filter_by(id=blog.type_id).first().name)
    categories = BlogType.query.all()
    loves = LoveMe.query.first()
    if loves is None:
        loves = 0
    else:
        loves = loves.counts
    return render_template('main/index.html', blogs=blogs, cates=cates, categories=categories, loves=loves)


@blog_bp.route('/blog/article/<blog_id>/')
def blog_article(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    blog.read_times += 1
    cate = BlogType.query.filter_by(id=blog.type_id).first()
    db.session.commit()
    return render_template('main/blog.html', blog=blog, cate=cate)


@blog_bp.route('/blog/cate/<cate_id>/', methods=['GET', 'POST'])
def blog_cate(cate_id):
    cate = BlogType.query.filter_by(id=cate_id).first()
    categories = BlogType.query.all()
    return render_template('main/blogCate.html', cate=cate, categories=categories, blogs=cate.blogs)


@blog_bp.route('/loveme/')
def love_me():
    love = LoveMe.query.first()
    if love is None:
        lv = LoveMe(counts=1)
        db.session.add(lv)
    else:
        love.counts += 1
    # 如果用户已经登录,则记录用户名 ip,否则记录 匿名用户 IP
    if current_user.is_authenticated:
        li = LoveInfo(user=current_user.username, user_ip=request.remote_addr)
    else:
        li = LoveInfo(user='Anonymous', user_ip=request.remote_addr)
    db.session.add(li)
    db.session.commit()
    flash('点赞成功!你们的支持就是我前进的动力啦~', 'success')
    return redirect(url_for('.index'))
