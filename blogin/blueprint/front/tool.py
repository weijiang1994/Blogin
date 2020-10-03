"""
# coding:utf-8
@Time    : 2020/9/30
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : tool
@Software: PyCharm
"""
from flask import Blueprint, render_template, request, jsonify, send_from_directory

from blogin.setting import basedir
from blogin.utils import allow_img_file, OCR, IPQuery, IP_REG, WordCloud
import re

tool_bp = Blueprint('tool_bp', __name__, url_prefix='/tool')


@tool_bp.route('/')
def index():
    return render_template('main/tool.html')


@tool_bp.route('/ocr/', methods=['GET', 'POST'])
def ocr():
    if request.method == 'POST':
        img = request.files['image']
        filename = img.filename
        if allow_img_file(filename):
            return jsonify({'tag': 0, 'info': '请上传jpg/png格式图片!'})
        img.save(basedir + '/uploads/ocr/' + filename)
        category = request.form.get('category')
        img_url = '/tool/ocr/' + filename
        c_ocr = OCR(filename=basedir + r'/uploads/ocr/' + filename, category=category)
        nums, texts = ocr_result(category, c_ocr)
        return jsonify({'tag': 1, 'nums': nums, 'texts': texts, 'img': img_url})
    return render_template("main/ocr.html")


@tool_bp.route('/query-ip/', methods=['GET', 'POST'])
def query_ip_addr():
    if request.method == 'POST':
        ip = request.form.get('ip')
        lang = request.form.get('lang')
        if not re.match(IP_REG, ip, flags=0):
            return jsonify({'tag': 0, 'info': '请输入正确的IP地址.'})
        ipq = IPQuery(ip=ip, lang=lang)
        result = ipq.query()
        region = [result[0], result[1], result[2]]
        region = '-'.join(region)
        return jsonify({'tag': 1, 'region': region, 'result': ipq.query()})

    return render_template('main/queryIP.html')


@tool_bp.route('/word-cloud/', methods=['GET', 'POST'])
def word_cloud():
    if request.method == 'POST':
        tag = request.form.get('tag')
        img = request.files['img']
        filename = img.filename
        img.save(basedir + '/uploads/wordcloud/' + filename)
        if tag == '0':
            content = request.form.get('content')
            wc = WordCloud(txt=content, img=basedir + '/uploads/wordcloud/' + filename)
            result = wc.generate()
        else:
            content = request.files['txt']
            content.save(basedir + '/uploads/wordcloud/' + content.filename)
            with open(basedir + '/uploads/wordcloud/' + content.filename) as f:
                content = f.read()
            wc = WordCloud(txt=content, img=basedir + '/uploads/wordcloud/' + filename)
            result = wc.generate()
        if result:
            return jsonify({'tag': 1, 'wc': '/tool/wordcloud/' + result,
                            'originImg': '/tool/wordcloud/' + filename})
        else:
            return jsonify({'tag': 0, 'info': '抱歉,词云生成出错了~'})
        return jsonify({'tag': 1})
    return render_template('main/wordCloud.html')


@tool_bp.route('/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = basedir + '/uploads/' + path + '/'
    return send_from_directory(path, filename)


def ocr_result(category, _ocr: OCR):
    if category == '文字识别':
        return _ocr.ocr()
    if category == '身份证识别':
        return _ocr.ocr_idcard()
    if category == '银行卡识别':
        return _ocr.ocr_bankcard()
    if category == '驾驶证识别':
        return _ocr.ocr_drive_card()
    if category == '车牌识别':
        return _ocr.ocr_license_plate()
