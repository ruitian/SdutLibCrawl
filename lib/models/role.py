# -*- coding: utf-8 -*-

from lib import db
from datetime import datetime


class Permission(object):
    ADMINISTER = 0x80


class RoleModel(db.Document):
    name = db.StringField(max_length=80, unique=True)
    permissions = db.IntField()
    created_time = db.DateTimeField(default=datetime.now, required=True)

    @staticmethod
    def insert_roles():
        roles = {
            'Administrator': (0xff)
        }
        for r in roles:
            role = RoleModel.objects(name=r).first()
            if role is None:
                role = RoleModel(name=r)
            role.permissions = roles[r][0]
            # role.default = roles[r][0]
            role.save()

    def __unicode__(self):
        return self.name
