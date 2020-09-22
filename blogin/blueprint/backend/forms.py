"""
# coding:utf-8
@Time    : 2020/9/22
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : forms
@Software: PyCharm
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectField, TextAreaField, FileField, SubmitField
from wtforms.validators import Length, DataRequired


class PostForm(FlaskForm):
    title = StringField(u'博客标题', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': '输入您的博客标题'})
    blog_type = SelectField(label=u'博客类型',
                            default=0,
                            coerce=int,
                            choices=[(1, 'Python'), (2, 'PHP')])
    blog_level = SelectField(label=u'博客权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'博客简介', validators=[DataRequired()])
    blog_img_file = FileField(label=u'博客示例图',
                              validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                              render_kw={'value': "上传", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField(u'发布博客')
