"""
# coding:utf-8
@Time    : 2020/10/13
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : other_bp
@Software: PyCharm
"""
import os
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
    app_log_path = basedir + '/logs/'
    nginx_log_path = '/var/log/nginx/'

    # 运行日志
    get_log_file_info(app_log_path, logs)
    get_log_file_info(nginx_log_path, logs, log_cate='nginx access/error 文件日志!')
    # nginx 日志
    # nginx_access_log_update_time = get_file_mtime('/var/log/nginx/access.log')
    # nginx_access_log_size = os.path.getsize('/var/log/nginx/access.log')
    #
    # nginx_error_log_update_time = get_file_mtime('/var/log/nginx/error.log')
    # nginx_error_log_size = os.path.getsize('/var/log/nginx/error.log')

    # logs.append(['access.log', 'nginx access文件日志!', nginx_access_log_update_time, '/var/log/nginx/access.log',
    #              str(nginx_access_log_size) + 'byte'])
    # logs.append(['error.log', 'nginx error文件日志!', nginx_error_log_update_time, '/var/log/nginx/error.log',
    #              str(nginx_error_log_size) + 'byte'])
    return render_template('backend/logs.html', logs=logs)


def get_log_file_info(app_log_path, logs, log_cate='程序运行日志！'):
    for app_log in get_log_files(app_log_path):
        app_log_update_time = get_file_mtime(app_log)
        app_log_size = os.path.getsize(app_log)
        logs.append(
            [os.path.split(app_log)[1], log_cate, app_log_update_time, app_log, str(app_log_size) + 'byte'])


@other_bp.route('/logs/detail/<path:file_path>/')
def log_detail(file_path):
    contents = []
    with open('/' + file_path) as f:
        for line in f.readlines():
            line.strip('\n')
            if line.__contains__('[GET]') or line.__contains__('[POST]'):
                line = "<span style='color: red;'>" + line + "</span>"
            if line.__contains__('Traceback'):
                line = "<span style='color: red;'>" + line + "</span>"
            contents.append(line)
    return render_template('backend/logDetail.html', contents=contents, path='/' + file_path)


def get_file_mtime(path):
    timestamp = os.path.getmtime(path)
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp


def get_log_files(path):
    fl_ls = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.__contains__('log'):
                fl_ls.append(os.path.join(root, f))
    return fl_ls
