from datetime import date
from sqlalchemy import exc
import errors
from app import db


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def del_id(self):
        db.session.delete(self)
        db.session.commit()
        return True

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck


class Ads(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(120))
    creator = db.Column(db.String(64))
    create_up = db.Column(db.String(64))

    def __str__(self):
        return f'{self.id} -- {self.title}'

    def __repr__(self):
        return str(self)

    def set_date(self):
        day = date.today()
        day_str = str(day)
        self.create_up = day_str

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'create_up': self.create_up,
            'creator': self.creator
        }
