# -*- coding: utf-8 -*-

from lib import db, login_manager
# from flask.ext.login import UserMixin
import base64
from mongoengine import NULLIFY


@login_manager.user_loader
def load_user(id):
    return VarifyItem.objects(id=id).first()


class VarifyItem(db.Document):
    number = db.StringField(max_length=128)
    passwd = db.StringField(max_length=128)
    status = db.StringField(default='False')
    meta = {
        'collection': 'VarifyItem'
    }


class AccountItem(db.Document):
    id = db.SequenceField(primary_key=True)
    number = db.StringField(max_length=128)
    passwd = db.StringField(max_length=128)
    books = db.DictField()

    meta = {
        'collection': 'AccountItem',
        # 'indexes': ['id', 'barcode']
    }


class UserModel(db.Document):
    id = db.SequenceField(primary_key=True)
    number = db.StringField(max_length=128)
    passwd = db.StringField(max_length=128)
    library = db.ReferenceField(VarifyItem, reverse_delete_rule=NULLIFY)

    @staticmethod
    def generate_password(password):
        password_encode = base64.b64encode(password)
        return password_encode

    @classmethod
    def create_user(cls, username, password, **kwargs):
        password = cls.generate_password(password)
        return cls.objects.create(
            username=username,
            password=password,
            **kwargs
        )

    meta = {
        'collection': 'User'
    }
