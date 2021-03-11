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
from flask import make_response, Blueprint
from blogin.models import Blog

rss_bp = Blueprint('rss_bp', __name__, url_prefix='/rss-feed/')


@rss_bp.route('/')
def rss_feed():
    blogs = Blog.query.filter_by(delete_flag=1).order_by(Blog.create_time.desc()).all()
    fg = FeedGenerator()
    fg.title('Blogin')
    fg.description('Blogin是一个个人博客网站，后端使用Flask框架，前端使用Bootstrap4，主要分享一些编程类的技术以及一些陈词滥调的文章!')
    fg.link(href='https://2dogz.cn')
    fg.language('zh')
    fg.id(str(len(blogs)))
    for blog in blogs:
        fe = fg.add_entry()
        fe.title(blog.title)
        fe.id(blog.id)
        fe.link(href='https://2dogz.cn//blog/article/{}/'.format(blog.id))
        fe.description(blog.introduce)
        fe.guid(str(blog.id), permalink=False)  # Or: fe.guid(article.url, permalink=True)
        fe.author(name='Blogin', email='weijiang1994_1@qq.com')
        fe.content(blog.content)
        # fe.category(category=[blog.blog_types.name])
        # fe.pubDate(blog.create_time)

    response = make_response(fg.atom_str(pretty=True))
    response.headers.set('Content-Type', 'application/rss+xml')
    return response
