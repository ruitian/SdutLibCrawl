# -*- coding: utf-8 -*-

from flask import url_for, redirect
from flask.views import MethodView
from flask.ext.login import logout_user, login_required


class LogoutView(MethodView):

    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('index.index'))
