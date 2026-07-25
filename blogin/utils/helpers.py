"""
# coding:utf-8
General-purpose helper utilities.
"""
import datetime
import hashlib
import json
import logging
import os
import random
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from flask import request, redirect, url_for


def is_empty(value, show=None):
    if len(value) > 0:
        return value
    if len(value) == 0 and show:
        return show


def format_json(code, indent):
    return json.dumps(code, indent=int(indent), ensure_ascii=False, separators=(',', ': '))


def format_html(code):
    soup = BeautifulSoup(code, 'html.parser')
    return soup.prettify()


def format_python(code):
    from blogin.setting import basedir
    fn = basedir + '/uploads/code-format/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.py'
    with open(fn, 'w') as f:
        f.write(code)
    res = os.system('black ' + fn)
    not_done = res != 0
    timeout = 0
    while not_done and timeout < 1000:
        not_done = False
        timeout += 1
    with open(fn, 'r') as f:
        return f.read()


def get_current_time():
    """Get the current time in YYYY-MM-DD HH:MM:SS format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def generate_ver_code():
    return random.randint(134299, 873242)


def split_space(string):
    return str(string).split()


def super_split(string, f):
    return str(string).split(f)


def conv_list(string):
    return list(string)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog_bp.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allow_img_file(filename):
    suffix = filename.rsplit('.', 1)[-1].lower()
    if suffix not in ['jpg', 'png', 'jpeg']:
        return False
    return True


def allow_txt_file(filename):
    suffix = filename.rsplit('.', 1)[-1].lower()
    if suffix != 'txt':
        return False
    return True


def get_md5(s):
    m = hashlib.md5()
    if isinstance(s, str):
        m.update(s.encode('utf-8'))
    return m.hexdigest()


def log_util(log_name, log_path, max_size=2 * 1024 * 1024, backup_count=10):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    logger = logging.getLogger(log_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = RotatingFileHandler(log_path + '/' + log_name,
                                       maxBytes=max_size,
                                       backupCount=backup_count,
                                       encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
