"""
# coding:utf-8
Statistics models with shared base class.
"""
from datetime import date

from blogin.extension import db


class BaseStatistics(db.Model):
    """Abstract base for daily statistics counters."""
    __abstract__ = True

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    times = db.Column(db.INTEGER, default=1)


class VisitStatistics(BaseStatistics):
    __tablename__ = 'visit_statistics'


class CommentStatistics(BaseStatistics):
    __tablename__ = 'comment_statistics'


class LikeStatistics(BaseStatistics):
    __tablename__ = 'like_statistics'
