# -*- coding: utf-8 -*-

from flask import Blueprint
from .login import LoginView
from .logout import LogoutView

bp_auth = Blueprint('auth', __name__)

bp_auth.add_url_rule(
    '/login',
    endpoint='login',
    view_func=LoginView.as_view('login'),
    methods=['GET', 'POST']
)

bp_auth.add_url_rule(
    '/logout',
    endpoint='logout',
    view_func=LogoutView.as_view('logout'),
    methods=['GET']
)
