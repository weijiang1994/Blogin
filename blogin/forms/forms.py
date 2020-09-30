"""
# coding:utf-8
@Time    : 2020/9/30
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : forms
@Software: PyCharm
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, FileField

choices = [(1, '文字识别'),(2, '文字识别')]

class OCRForm(FlaskForm):

    category = SelectField(choices=[(1, )])