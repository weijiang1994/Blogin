"""
# coding:utf-8
@Time    : 2020/9/30
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : tool
@Software: PyCharm
"""
import os
import random

from PIL import Image
from flask import Blueprint, render_template, request, jsonify, send_from_directory, flash, abort

from blogin.setting import basedir
from blogin.utils import allow_img_file, OCR, IPQuery, IP_REG, WordCloud, GoogleTranslation, TRAN_LANGUAGE, \
    BaiduTranslation, BAIDU_LANGUAGE, YoudaoTranslation, FONT_COLOR, AddMark2RT, AddMark2RB, \
    AddMark2LT, AddMark2LB, AddMark2Rotate, AddMark2Center, AddMark2Parallel, resize_img
import re
from blogin.models import SongCi, Poem, Poet, SongCiAuthor

tool_bp = Blueprint('tool_bp', __name__, url_prefix='/tool')

MARK_POSITION = {'右上角': AddMark2RT,
                 '右下角': AddMark2RB,
                 '左上角': AddMark2LT,
                 '左下角': AddMark2LB,
                 '中心': AddMark2Center,
                 '水平铺满': AddMark2Parallel,
                 '45°铺满': AddMark2Rotate}


@tool_bp.route('/')
def index():
    return render_template('main/tool/tool.html')


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
    return render_template("main/tool/ocr.html")


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

    return render_template('main/tool/queryIP.html')


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
            size = os.path.getsize(basedir + '/uploads/wordcloud/' + content.filename)
            if size > 1700000:
                os.remove(basedir + '/uploads/wordcloud/' + content.filename)
                return jsonify({'tag': 0, 'info': '上传txt请小于1.6M!'})
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
    return render_template('main/tool/wordCloud.html')


@tool_bp.route('/multi-translation/', methods=['GET', 'POST'])
def multi_translation():
    if request.method == 'POST':
        try:
            tran_type = request.form.get('type')
            text = request.form.get('text')
            google_res = GoogleTranslation().query(text, lang_to=TRAN_LANGUAGE.get(tran_type))
            baidu_res = BaiduTranslation(q=text, lang=BAIDU_LANGUAGE.get(tran_type)).query()
            youdao_res = YoudaoTranslation(q=text, to_lang=BAIDU_LANGUAGE.get(tran_type)).query()
            return jsonify({'tag': 1, 'googleRes': google_res, 'baiduRes': baidu_res, 'youdaoRes': youdao_res})
        except:
            import traceback
            traceback.print_exc()
            return jsonify({'tag': 0, 'info': '可能由于请求过多，导致翻译服务器拒绝连接，请稍后重试!'})
    return render_template('main/tool/translation.html')


@tool_bp.route('/image-pro/', methods=['GET', 'POST'])
def image_pro():
    if request.method == 'POST':
        img = request.files['image']
        if os.path.splitext(img.filename)[1] not in ['.jpg', '.png', '.jpeg', '.bmp']:
            return jsonify({'tag': 0, 'info': '目前支持jpg/png/jpeg/bmp类型图片!'})
        pro_type = request.form.get('proType')

        origin_img_path = basedir + '/uploads/img-pro/' + img.filename
        img.save(origin_img_path)

        if pro_type == '添加水印':
            mark_text = request.form.get('markText')
            font_size = request.form.get('markTextSize')
            font_color = request.form.get('markFontColor')
            mark_position = request.form.get('markPosition')

            pro_img_filename = mark_position + '_mark_' + font_color + '_' + os.path.splitext(img.filename)[0] + '.png'
            save_path = basedir + '/uploads/img-pro/' + pro_img_filename
            img_stream = Image.open(origin_img_path)
            MARK_POSITION.get(mark_position)(font_color=FONT_COLOR.get(font_color), font_size=int(font_size),
                                             image=img_stream, text=mark_text, save_path=save_path).generate_mark()
            return jsonify({'originPath': '/tool/img-pro/' + img.filename, 'proPath':
                '/tool/img-pro/' + pro_img_filename})

        if pro_type == '图片缩放':
            width_zoom = request.form.get('widthZoom', type=float)
            height_zoom = request.form.get('heightZoom', type=float)
            pro_img = resize_img(origin_img_path, w_zoom=width_zoom, h_zoom=height_zoom)
            img_name = os.path.split(origin_img_path)[1]
            pre_num = random.randint(0, 3456)
            pro_img.save(basedir + r'/uploads/img-pro/' + 'resize' + str(pre_num) + img_name)
            return jsonify({'originPath': '/tool/img-pro/' + img.filename, 'proPath':
                '/tool/img-pro/' + 'resize' + str(pre_num) + img_name})

        if pro_type == '证件照换底':
            pass

    return render_template('main/tool/image-pro.html')


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


@tool_bp.route('/poem-tang/')
def poem_tang():
    return render_template('main/tool/tang-poem.html')


@tool_bp.route('/poem-song/')
def poem_song():
    return render_template('main/tool/song-poem.html')


@tool_bp.route('/ci-song/')
def ci_song():
    return render_template('main/tool/song-ci.html')


@tool_bp.route('/search/')
def search():
    type1 = request.args.get('searchType')
    type2 = request.args.get('searchType2')
    mode = request.args.get('searchType3')
    keyword = request.args.get('keyword')
    per_page = request.args.get('perPage', 50, type=int)
    page = request.args.get('page', 1, type=int)
    if type1 is not None:
        if keyword.strip() == '':
            flash('小伙你很皮，空的关键字你能搜到个G2东西?', 'danger')
            return render_template('main/tool/search.html')

        if type1 == '诗':
            if type2 == '作者':
                if mode == '精确查询':
                    poet = Poet.query.filter_by(name=keyword).first()
                    if poet is None:
                        flash('数据库中未找到相关作者信息,请查正后再试!', 'danger')
                        return render_template('main/tool/search.html', tag=0)
                    pagination = Poem.query.filter_by(author_id=poet.id).paginate(page=page, per_page=per_page)
                    results = pagination.items
                if mode == '模糊查询':
                    flash('作者不支持模糊查询方式!', 'danger')
                    return render_template('main/tool/search.html', tag=0)

            if type2 == '标题':
                if mode == '精确查询':
                    pagination = Poem.query.filter_by(title=keyword).paginate(page=page, per_page=per_page)
                    results = pagination.items
                if mode == '模糊查询':
                    pagination = Poem.query.filter(Poem.title.like('%{}%'.format(keyword))).paginate(page=page,
                                                                                                     per_page=per_page)
                    results = pagination.items
            if type2 == '内容':
                if mode == '精确查询':
                    flash('诗词内容不支持精确查询的方式!', 'danger')
                    return render_template('main/tool/search.html', tag=0)
                if mode == '模糊查询':
                    pagination = Poem.query.filter(Poem.content.like('%{}%'.format(keyword))).paginate(page=page, per_page=per_page)
                    results = pagination.items

        if type1 == '词':
            if type2 == '作者':
                if mode == '精确查询':
                    author = SongCiAuthor.query.filter_by(name=keyword).first()
                    if author is None:
                        flash('数据库中未找到相关作者信息,请查正后再试!', 'danger')
                        return render_template('main/tool/search.html', tag=0)
                    pagination = SongCi.query.filter_by(author_id=author.id).paginate(page=page, per_page=per_page)
                    results = pagination.items
                if mode == '模糊查询':
                    flash('作者不支持模糊查询方式!', 'danger')
                    return render_template('main/tool/search.html', tag=0)
            if type2 == '标题':
                if mode == '精确查询':
                    pagination = SongCi.query.filter_by(rhythmic=keyword).paginate(page=page, per_page=per_page)
                    results = pagination.items
                if mode == '模糊查询':
                    pagination = SongCi.query.filter(SongCi.rhythmic.like('%{}%'.format(keyword))).\
                        paginate(page=page, per_page=per_page)
                    results = pagination.items

            if type2 == '内容':
                if mode == '精确查询':
                    flash('诗词内容不支持精确查询的方式!', 'danger')
                    return render_template('main/tool/search.html', tag=0)
                if mode == '模糊查询':
                    pagination = SongCi.query.filter(SongCi.content.like('%{}%'.format(keyword))).paginate(page=page,
                                                                                              per_page=per_page)
                    results = pagination.items

        return render_template('main/tool/search.html', tag=1, results=results, pagination=pagination, sctype=type1,
                               mode=mode, keyword=keyword, type2=type2)
    return render_template('main/tool/search.html', tag=0)
