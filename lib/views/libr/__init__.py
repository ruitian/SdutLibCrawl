# -*- coding: utf-8 -*-

from flask import Blueprint
from .login import LoginView

bp_libr = Blueprint('libr', __name__)

bp_libr.add_url_rule(
    '/login',
    endpoint='login',
    view_func=LoginView.as_view('login'),
    methods=['get', 'post']
)
