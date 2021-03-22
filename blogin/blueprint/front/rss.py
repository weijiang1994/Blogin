"""
# coding:utf-8
@Time    : 2021/03/11
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : rss.py
@Desc    : rss
@Software: PyCharm
"""
from feedgen.feed import FeedGenerator
from flask import make_response, Blueprint, render_template, request, url_for
from blogin.models import Blog, BlogType
from blogin.blueprint.front.tool import to_html

rss_bp = Blueprint('rss_bp', __name__, url_prefix='/rss-feed/')


def generate_rss(blogs):
    fg = FeedGenerator()
    fg.title('Blogin')
    fg.description('Blogin是一个个人博客网站，后端使用Flask框架，前端使用Bootstrap4，主要分享一些编程类的技术以及一些陈词滥调的文章!')
    fg.link(href='https://2dogz.cn')
    fg.id(str(len(blogs)))
    for blog in blogs:
        fe = fg.add_entry()
        fe.title('[{}]'.format(blog.blog_types.name) + blog.title)
        fe.id(blog.id)
        fe.link(href='https://2dogz.cn//blog/article/{}/'.format(blog.id))
        fe.description(blog.introduce)
        fe.guid(str(blog.id), permalink=False)  # Or: fe.guid(article.url, permalink=True)
        fe.author(name='Blogin', email='weijiang1994_1@qq.com')
        fe.content(blog.content)
    return fg


@rss_bp.route('/index/')
def rss_index():
    cates = BlogType.query.all()
    blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
    fg = generate_rss(blogs)
    rss_data = str(fg.atom_str(pretty=True), 'utf-8')
    return render_template('main/rss.html', cates=cates, response=rss_data)


@rss_bp.route('/')
def rss_feed():
    blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
    fg = generate_rss(blogs)
    rss_data = str(fg.atom_str(pretty=True), 'utf-8')
    response = make_response(rss_data)
    response.headers.set('Content-Type', 'rss+xml')
    return response


@rss_bp.route('/category/<cate_id>/')
def rss_category_feed(cate_id):
    blogs = Blog.query.filter(Blog.delete_flag == 1, Blog.type_id == cate_id).order_by(Blog.create_time.desc()).all()
    fg = generate_rss(blogs)
    rss_data = str(fg.atom_str(pretty=True), 'utf-8')
    response = make_response(rss_data)
    response.headers.set('Content-Type', 'rss+xml')
    return response


@rss_bp.route('/display-rss/', methods=['POST'])
def display_rss():
    cate_id = request.form.get('cate-id')
    url = url_for('.rss_category_feed', cate_id=cate_id, _external=True)
    if cate_id == 'all':
        blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
        url = url_for('.rss_feed', _external=True)
    else:
        blogs = Blog.query.filter(Blog.delete_flag == 1, Blog.type_id == cate_id).order_by(Blog.create_time.desc()).all()
    fg = generate_rss(blogs)
    rss_data = str(fg.atom_str(pretty=True), 'utf-8')
    return {'url': url, 'xml': rss_data}
