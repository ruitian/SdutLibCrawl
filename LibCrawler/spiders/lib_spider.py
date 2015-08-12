# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request  # noqa
from scrapy.selector import Selector  # noqa
from LibCrawler.items import VarifyItem


class VarifySpider(scrapy.Spider):

    name = 'varify'
    allowed_domains = ['lib.sdut.edu.cn']
    login_url = 'http://222.206.65.12/reader/redr_verify.php'

    is_login = False

    def __init__(
        self,
        number,
        passwd,
        select='cert_no',
        *args, **kwargs
    ):
        super(VarifySpider, self).__init__(*args, **kwargs)
        self.number = number
        self.passwd = passwd
        self.select = select

    def start_requests(self):

        return [FormRequest(
            self.login_url,
            formdata={
                'number': self.number,
                'passwd': self.passwd,
                'select': self.select
            },
            callback=self.after_login,
            dont_filter=True
        )]

    def after_login(self, response):
        item = VarifyItem()
        if response.url != self.login_url:
            self.is_login = True
            item['number'] = self.number
            item['passwd'] = self.passwd
            item['status'] = 'True'
        else:
            item['number'] = self.number
            item['passwd'] = self.passwd
            item['status'] = 'False'
        yield item
