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
from blogin.utils import allow_img_file, OCR

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
        img.save(basedir+'/uploads/ocr/'+filename)
        category = request.form.get('category')
        img_url = '/tool/ocr/'+filename
        c_ocr = OCR(filename=basedir + r'/uploads/ocr/'+filename, category=category)
        results = c_ocr.ocr()
        nums = results.get('words_result_num')
        texts = ''
        for text in results.get('words_result'):
            texts += text.get('words') + '\n'
        return jsonify({'tag': 1, 'nums': nums, 'texts': texts, 'img': img_url})
    return render_template("main/ocr.html")


@tool_bp.route('/<path>/<filename>')
def get_blog_sample_img(path, filename):
    path = basedir + '/uploads/' + path + '/'
    return send_from_directory(path, filename)
