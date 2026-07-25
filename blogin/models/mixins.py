"""
# coding:utf-8
Models package — shared mixins.
"""
from datetime import datetime, date

from sqlalchemy.ext.declarative import declared_attr

from blogin.extension import db


class TimeMixin:
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.now)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Mixin:

    def to_dict(
            self,
            datetime_fmt='%Y-%m-%d %H:%M:%S',
            date_fmt='%Y-%m-%d',
            special_col={}
    ):
        result = {}
        for col in self.__table__.columns:
            if col.name in special_col.keys():
                result[col.name] = special_col.get(col.name)(getattr(self, col.name))
            elif isinstance(getattr(self, col.name), datetime):
                result[col.name] = getattr(self, col.name).strftime(datetime_fmt)
            elif isinstance(getattr(self, col.name), date):
                result[col.name] = getattr(self, col.name).strftime(date_fmt)
            else:
                result[col.name] = getattr(self, col.name)
        return result

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.save()
