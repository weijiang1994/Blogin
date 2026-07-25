"""
# coding:utf-8
Poetry models: Poet, Dynasty, Poem, SongCi, SongCiAuthor.
"""
from blogin.extension import db


class Dynasty(db.Model):
    __tablename__ = 'dynasty'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    poets = db.relationship('Poet', back_populates='dynasties', cascade='all')


class Poet(db.Model):
    """唐宋诗人表"""
    __tablename__ = 'poet'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    desc = db.Column(db.TEXT, default='')
    dynasty_id = db.Column(db.INTEGER, db.ForeignKey('dynasty.id'))
    json_id = db.Column(db.String(100), unique=True)

    dynasties = db.relationship('Dynasty', back_populates='poets')
    poems = db.relationship('Poem', back_populates='poets', cascade='all')


class Poem(db.Model):
    __tablename__ = 'poem'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    author_id = db.Column(db.INTEGER, db.ForeignKey('poet.id'))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.TEXT, nullable=False)

    poets = db.relationship('Poet', back_populates='poems')


class SongCiAuthor(db.Model):
    __tablename__ = 'song_ci_author'

    id = db.Column(db.INTEGER, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    s_desc = db.Column(db.TEXT)
    desc = db.Column(db.TEXT)

    cis = db.relationship('SongCi', back_populates='authors', cascade='all')


class SongCi(db.Model):
    __tablename__ = 'song_ci'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    author_id = db.Column(db.INTEGER, db.ForeignKey('song_ci_author.id'))
    rhythmic = db.Column(db.String(100), nullable=False)
    content = db.Column(db.TEXT, nullable=False)

    authors = db.relationship('SongCiAuthor', back_populates='cis')
