"""
# coding:utf-8
Image watermarking, OCR, and thumbnail utilities.
"""
import base64
import datetime
import os

import requests
from PIL import Image, ImageDraw, ImageFont
from imageio import imread
import jieba
import wordcloud as wc
from wordcloud import STOPWORDS

from blogin.setting import basedir
from blogin.utils.constants import OCR_URL, OCR_TOKEN, OCR_HEADERS, OCR_CATEGORY, BANK_CARD_TYPE


class ImageAddMarkBase:
    def __init__(self, image, text, font_size, save_path, font_color):
        self.image = image
        self.text = text
        self.font_size = font_size
        self.save_path = save_path
        self.font_color = font_color
        self.font = None
        self.font_len = None
        self.image_draw = None
        self.rgba_image = None
        self.text_overlay = None

    def generate_base(self):
        self.font = ImageFont.truetype(basedir + '/res/STFangsong.ttf', self.font_size)
        new_img = Image.new('RGBA', (self.image.size[0] * 3, self.image.size[1] * 3), (0, 0, 0, 0))
        new_img.paste(self.image, self.image.size)

        self.font_len = len(self.text)
        self.rgba_image = new_img.convert('RGBA')
        self.text_overlay = Image.new('RGBA', self.rgba_image.size, (255, 255, 255, 0))
        self.image_draw = ImageDraw.Draw(self.text_overlay)


class AddMark2RT(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2RT, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        self.image_draw.text((self.image.size[0] * 2 - (self.font_len + 150), self.image.size[1]),
                             self.text, font=self.font, fill=self.font_color)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


class AddMark2RB(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2RB, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        self.image_draw.text((self.image.size[0] * 2 - (self.font_len * self.font_size),
                              self.image.size[1] * 2 - (self.font_len * (self.font_size / 3))),
                             self.text, font=self.font, fill=self.font_color)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


class AddMark2LT(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2LT, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        self.image_draw.text((self.image.size[0], self.image.size[1]),
                             self.text, font=self.font, fill=self.font_color)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


class AddMark2LB(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2LB, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        self.image_draw.text((self.image.size[0], self.image.size[1] * 2 - (self.font_len * (self.font_size / 3))),
                             self.text, font=self.font, fill=self.font_color)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


class AddMark2Center(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2Center, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        self.image_draw.text((self.image.size[0] * 1.5 - self.font_len, self.image.size[1] * 1.5),
                             self.text, font=self.font, fill=self.font_color)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


class AddMark2Parallel(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2Parallel, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        for i in range(0, self.rgba_image.size[0], self.font_len * self.font_size + 50):
            for j in range(0, self.rgba_image.size[1], int(self.image.size[1] / 10)):
                self.image_draw.text((i, j), self.text, font=self.font, fill=self.font_color)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


class AddMark2Rotate(ImageAddMarkBase):
    def __init__(self, *args, **kwargs):
        super(AddMark2Rotate, self).__init__(*args, **kwargs)
        self.generate_base()

    def generate_mark(self):
        for i in range(0, self.rgba_image.size[0], self.font_len * 40 + 50):
            for j in range(0, self.rgba_image.size[1], int(self.image.size[1] / 10)):
                self.image_draw.text((i, j), self.text, font=self.font, fill=self.font_color)
        self.text_overlay = self.text_overlay.rotate(-45)
        image_with_text = Image.alpha_composite(self.rgba_image, self.text_overlay)
        image_with_text = image_with_text.crop(
            (self.image.size[0], self.image.size[1], self.image.size[0] * 2, self.image.size[1] * 2))
        image_with_text.save(self.save_path)


def add_mark_to_image(image, text, font_size, save_path, font_color):
    font = ImageFont.truetype(basedir + '/res/STFangsong.ttf', font_size)
    new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (0, 0, 0, 0))
    new_img.paste(image, image.size)

    font_len = len(text)
    rgba_image = new_img.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    for i in range(0, rgba_image.size[0], font_len * 40 + 50):
        for j in range(0, rgba_image.size[1], 100):
            image_draw.text((i, j), text, font=font, fill=font_color)

    text_overlay = text_overlay.rotate(-45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    image_with_text.save(save_path)


def resize_img(path, w_zoom, h_zoom):
    """
    生成缩略图
    :param h_zoom: 高放大比例
    :param w_zoom: 宽放大比例
    :param path: 文件路径
    :return: 返回缩略图，缩小尺寸到原来的三分之一
    """
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.resize((int(width * w_zoom), int(height * h_zoom)), Image.ANTIALIAS)
    return img


def generate_thumbnail(path):
    """
    生成缩略图
    :param path: 文件路径
    :return: 返回缩略图，缩小尺寸到原来的三分之一
    """
    img = Image.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width = img.size[0]
    height = img.size[1]
    img = img.resize((int(width * 0.3), int(height * 0.3)), Image.ANTIALIAS)
    return img


class OCR:
    def __init__(self, filename, category='accurate_basic'):
        self.filename = filename
        self.category = category
        self.url = None
        self.img = None
        self.set_url()
        self.set_img()

    def set_url(self):
        self.url = OCR_URL + OCR_CATEGORY.get(self.category) + "?access_token=" + OCR_TOKEN

    def set_img(self):
        with open(self.filename, 'rb') as f:
            self.img = base64.b64encode(f.read())

    def ocr(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        nums = res.get("words_result_num")
        texts = ''
        for text in res.get('words_result'):
            texts += text.get('words') + '\n'
        return nums, texts

    def ocr_idcard(self):
        response = requests.post(self.url, data={"id_card_side": "front", "image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        nums = res.get('words_result_num')
        texts = ''
        results = res.get('words_result')
        texts += '姓名:' + results.get('姓名').get('words') + '\n'
        texts += '民族:' + results.get('民族').get('words') + '\n'
        texts += '住址:' + results.get('住址').get('words') + '\n'
        texts += '出生:' + results.get('出生').get('words') + '\n'
        texts += '公民身份号码:' + results.get('公民身份号码').get('words') + '\n'
        texts += '性别:' + results.get('性别').get('words') + '\n'
        return nums, texts

    def ocr_bankcard(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        card_num = res.get('result').get('bank_card_number')
        validate_date = res.get('result').get('valid_date')
        card_type = BANK_CARD_TYPE.get(res.get('result').get('bank_card_type'))
        bank_name = res.get('result').get('bank_name')
        return 4, '卡号: ' + card_num + '\n' + '有效日期: ' + validate_date + \
               '\n' + '卡种: ' + card_type + '\n' + '所属行: ' + bank_name

    def ocr_drive_card(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        nums = res.get('words_result_num')
        results = res.get('words_result')
        number = results.get('证号').get('words')
        validate_date = results.get('有效期限').get('words')
        car_type = results.get('准驾车型').get('words')
        addr = results.get('住址').get('words')
        name = results.get('姓名').get('words')
        country = results.get('国籍').get('words')
        birth = results.get('出生日期').get('words')
        gender = results.get('性别').get('words')
        get_time = results.get('初次领证日期').get('words')

        return nums, ('证号: ' + number + '\n' + '有效期限: ' + validate_date + '\n' + '准驾车型: ' + car_type +
                      '\n' + '住址: ' + addr + '\n' + '姓名: ' + name + '\n' + '国籍: ' + country +
                      '\n' + '出生日期: ' + birth + '\n' + '性别: ' + gender + '\n' + '初次领证日期: ' + get_time)

    def ocr_license_plate(self):
        response = requests.post(self.url, data={"image": self.img}, headers=OCR_HEADERS)
        res = response.json()
        color = res.get('words_result').get('color')
        number = res.get('words_result').get('number')
        return 0, '车牌颜色: ' + color + '\n' + '车牌号码: ' + number


class WordCloud:
    def __init__(self, txt=None, img=None, bg='black'):
        self.txt = txt
        self.img = img
        self.words = None
        self.bg = bg

    def cut(self):
        self.words = jieba.cut(self.txt)
        self.words = ' '.join(self.words)

    def generate(self):
        try:
            mask = imread(self.img)
            self.cut()
            w = wc.WordCloud(collocations=False,
                             font_path=basedir + r'/res/STFangsong.ttf',
                             mask=mask,
                             background_color=self.bg,
                             mode='RGBA')
            w.generate(self.words)
            pre = str(datetime.datetime.now()).split(' ')[1].replace(':', '')
            w.to_file(basedir + '/uploads/wordcloud/' + pre + '.png')
            return pre + '.png'
        except Exception:
            import traceback
            traceback.print_exc()
            return False
