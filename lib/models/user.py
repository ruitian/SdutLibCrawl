# -*- coding: utf-8 -*-

from lib import db, login_manager
# from flask.ext.login import UserMixin
import base64
from mongoengine import NULLIFY


@login_manager.user_loader
def load_user(id):
    return AccountItem.objects(id=id).first()


class AccountItem(db.Document):
    username = db.StringField(max_length=128)
    password = db.StringField(max_length=128)
    status = db.StringField(default='False')
    books = db.DictField()
    '''
    barcode = db.StringField(max_length=128)
    title = db.StringField()
    author = db.StringField()
    data = db.StringField()
    backdata = db.StringField()
    '''


class Usermodel(db.Document):
    id = db.SequenceField(primary_key=True)
    username = db.StringField(max_length=128)
    password = db.StringField(max_length=128)
    library = db.ReferenceField(AccountItem, reverse_delete_rule=NULLIFY)

    @staticmethod
    def generate_password(password):
        password_encode = base64.b64encode(password)
        return password_encode

    @classmethod
    def create_account(cls, username, password):
        password = cls.generate_password(password)
        return cls.objects.create(
            username=username,
            password=password
        )

    meta = {
        'collection': 'AccountItem'
    }
