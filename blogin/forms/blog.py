"""
# coding:utf-8
@Time    : 2020/9/22
@Author  : jiangwei
@File    : forms
@Software: PyCharm
"""
from datetime import datetime

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectField, TextAreaField, FileField, SubmitField, DateTimeField, DateField
from wtforms.validators import Length, DataRequired, ValidationError
from blogin.models import BlogType, FriendLink


class PostForm(FlaskForm):
    title = StringField(u'博客标题', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': '输入您的博客标题'})
    blog_type = SelectField(label=u'博客类型',
                            default=0,
                            coerce=int)
    blog_level = SelectField(label=u'博客权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'博客简介', validators=[DataRequired()])
    blog_img_file = FileField(label=u'博客示例图',
                              validators=[DataRequired(), FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                              render_kw={'value': "上传", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired(message='请输入博客内容')])
    save = SubmitField(u'保存草稿')
    submit = SubmitField(u'发布博客')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        categories = BlogType.query.all()
        self.blog_type.choices = [(cate.id, cate.name) for cate in categories]


class EditPostForm(FlaskForm):
    title = StringField(u'博客标题', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': '输入您的博客标题'})
    blog_type = SelectField(label=u'博客类型', default=0, coerce=int)
    blog_level = SelectField(label=u'博客权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                             default=1, coerce=int)
    brief_content = TextAreaField(u'博客简介', validators=[DataRequired()])
    blog_img_file = FileField(u'博客示例图', validators=[FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                              render_kw={'value': "上传", 'class': 'btn btn-default'})
    body = CKEditorField('Body', validators=[DataRequired(message='请输入博客内容')])
    submit = SubmitField(u'保存编辑')

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        categories = BlogType.query.all()
        self.blog_type.choices = [(cate.id, cate.name) for cate in categories]


class AddPhotoForm(FlaskForm):
    # 添加相册照片前端表单
    photo_title = StringField(u'相片标题',
                              validators=[DataRequired(), Length(min=1, max=20, message='相片标题长度必须在1到20之间')],
                              render_kw={'class': '', 'rows': 50, 'placeholder': '输入照片标题'})
    photo_desc = TextAreaField(u'相片描述',
                               validators=[DataRequired(), Length(min=3, max=250, message='相片描述长度必须在3到250之间')])
    img_file = FileField(label=u'相片文件',
                         validators=[DataRequired(), FileAllowed(['png', 'jpg'], '只接收png和jpg图片')],
                         render_kw={'value': "上传", 'class': 'btn btn-default'})
    photo_level = SelectField(label=u'照片权限', choices=[(1, '公开'), (2, '私有')], validators=[DataRequired()],
                              default=1, coerce=int)
    tags = StringField(u'相片标签',
                       validators=[DataRequired(), Length(min=1, max=50, message='标签长度必须在1-50之间')],
                       render_kw={'placeholder': '请输入相片标签，用空格隔开'})
    submit = SubmitField(u'发布相片')


class EditPhotoInfoForm(FlaskForm):
    photo_title = StringField(u'相片标题',
                              validators=[DataRequired(), Length(min=1, max=20, message='相片标题长度必须在1到20之间')],
                              render_kw={'class': '', 'rows': 50, 'placeholder': '输入照片标题'})
    photo_desc = TextAreaField(u'相片描述',
                               validators=[DataRequired(), Length(min=3, max=250, message='相片描述长度必须在3到250之间')])
    submit = SubmitField(u'保存信息')


class TimelineForm(FlaskForm):
    timeline_title = StringField(u'名称', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                                 render_kw={'class': '', 'rows': 50, 'placeholder': '请输入时间线标题'})
    timeline_content = TextAreaField(u'时间线内容', validators=[DataRequired()],
                                     render_kw={'placeholder': '请输入时间线内容，多条使用；隔开以及使用；结尾！！',
                                                'style': 'height:150px;'})
    timestamp = DateTimeField(u'日期', default=datetime.now)
    submit = SubmitField(u'添加时间线')


class AddFlinkForm(FlaskForm):

    name = StringField(u'友链名称', validators=[DataRequired(), Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                       render_kw={'class': '', 'rows': 50, 'placeholder': '请输入友链名称'})
    link = StringField(u'URL地址', validators=[DataRequired(), Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                       render_kw={'class': '', 'rows': 50, 'placeholder': '请输入友链URL地址'})
    desc = StringField(u'友链描述', validators=[Length(min=3, max=50, message='用户名长度必须在3到20位之间')],
                       render_kw={'class': '', 'rows': 50, 'placeholder': '请输入友链描述信息'})
    submit = SubmitField(u'添加友链')

    def validate_name(self, filed):
        if FriendLink.query.filter_by(name=filed.data).first():
            raise ValidationError('该名称已存在')

    def validate_link(self, filed):
        if FriendLink.query.filter_by(link=filed.data.lower()).first():
            raise ValidationError('该URL已经被添加')


class AddPlanForm(FlaskForm):
    title = StringField(u'计划名称', validators=[DataRequired(),
                                                Length(min=2, max=20, message='计划标题长度在2-20个字符之间')],
                        render_kw={'class': '', 'rows': 50, 'placeholder': '请输入计划的标题名称'}
                        )
    total = StringField(u'总进度', validators=[DataRequired()],
                        render_kw={'class': '', 'rows': 50, 'type': 'number', 'placeholder': '请输入计划的总进度'}
                        )
    timestamps = DateField(u'开始时间', default=datetime.today())
    submit = SubmitField(u'添加计划')
