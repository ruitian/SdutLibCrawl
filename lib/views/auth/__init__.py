# -*- coding: utf-8 -*-

from flask import Blueprint
from .login import LoginView

bp_auth = Blueprint('auth', __name__)

bp_auth.add_url_rule(
    '/login',
    endpoint='login',
    view_func=LoginView.as_view('login'),
    methods=['get', 'post']
)
