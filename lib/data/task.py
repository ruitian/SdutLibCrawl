# -*- coding: utf-8 -*-

from lib import app
from celery import Celery

from crawler import VarifyCrawler, BooksCrawler
from lib.models import VarifyItem, AccountItem


def make_celery(app):
    celery = Celery(
        app.name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@celery.task()
def login(number, passwd):
    crawler = VarifyCrawler()
    crawler.crawl(
        number,
        passwd,
    )


@celery.task()
def varify_login(number):
    user = VarifyItem.objects(number=number).first()
    if user.status == 'True':
        return {'number': user.number, 'passwd': user.passwd}
    else:
        return False


@celery.task()
def books(number, passwd):
    crawler = BooksCrawler()
    crawler.crawl(
        number,
        passwd
    )


@celery.task()
def get_books(number):
    user = AccountItem.objects(number=number).first()
    if user is not None:
        return user
