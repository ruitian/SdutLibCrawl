# -*- coding: utf-8 -*-

from lib import app
from celery import Celery

from crawler import AccountCrawler


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
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
def account_init(username, password):
    crawler = AccountCrawler()
    crawler.crawl(
        username,
        password
    )


@celery.task()
def test(a, b):
    return a+b