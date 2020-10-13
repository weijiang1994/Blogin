"""
# coding:utf-8
@Time    : 2020/10/13
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : other_bp
@Software: PyCharm
"""
from datetime import datetime

from flask import Blueprint, render_template

from blogin import basedir

other_bp = Blueprint('other_bp', '__name__', url_prefix='/backend')


@other_bp.route('/timeline/add/')
def add_timeline():
    pass


@other_bp.route('/logs/')
def look_logs():
    logs = []
    import os
    # 运行日志
    app_log_update_time = os.path.getmtime(basedir + '/logs/blogin.log')
    app_log_update_time = get_file_mtime(app_log_update_time)
    app_log_size = os.path.getsize(basedir + '/logs/blogin.log')
    # nginx 日志
    nginx_access_log_update_time = os.path.getmtime('/var/log/nginx/access.log')
    nginx_access_log_update_time = get_file_mtime(nginx_access_log_update_time)
    nginx_access_log_size = os.path.getsize('/var/log/nginx/access.log')

    nginx_error_log_update_time = os.path.getmtime('/var/log/nginx/error.log')
    nginx_error_log_update_time = get_file_mtime(nginx_error_log_update_time)
    nginx_error_log_size = os.path.getsize('/var/log/nginx/error.log')

    logs.append(['blog.log', '程序运行日志!', app_log_update_time, basedir + '/logs/blogin.log', str(app_log_size) + 'byte'])
    logs.append(['access.log', 'nginx access文件日志!', nginx_access_log_update_time, '/var/log/nginx/access.log',
                 str(nginx_access_log_size) + 'byte'])
    logs.append(['error.log', 'nginx error文件日志!', nginx_error_log_update_time, '/var/log/nginx/error.log',
                 str(nginx_error_log_size) + 'byte'])
    return render_template('backend/logs.html', logs=logs)


@other_bp.route('/logs/detail/<path:file_path>/')
def log_detail(file_path):
    contents = []
    with open('/' + file_path) as f:
        for line in f.readlines():
            contents.append(line.strip('\n'))
    return render_template('backend/logDetail.html', contents=contents, path='/'+file_path)


def get_file_mtime(timestamp):
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp
