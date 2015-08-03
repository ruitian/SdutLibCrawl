# -*- coding: utf-8 -*-

from flask import render_template
from lib.forms import LoginForm  # noqa

from flask.views import MethodView


class IndexView(MethodView):

    def get():
        return render_template('index.html')
