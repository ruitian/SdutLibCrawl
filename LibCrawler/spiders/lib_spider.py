# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request  # noqa
from scrapy.selector import Selector  # noqa
from LibCrawler.items import VarifyItem, AccountItem


class VarifySpider(scrapy.Spider):

    name = 'varify'
    allowed_domains = ['lib.sdut.edu.cn']
    login_url = 'http://222.206.65.12/reader/redr_verify.php'

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
            item['number'] = self.number
            item['passwd'] = self.passwd
            item['status'] = 'True'
        else:
            item['number'] = self.number
            item['passwd'] = self.passwd
            item['status'] = 'False'
        yield item


class BookSpider(scrapy.Spider):

    name = 'books'
    allowed_domains = ['lib.sdut.edu.cn']
    login_url = 'http://222.206.65.12/reader/redr_verify.php'
    start_urls = [
        'http://222.206.65.12/reader/book_lst.php'
    ]

    books = {}

    is_login = False

    def __init__(
        self,
        number,
        passwd,
        select='cert_no',
        *args, **kwargs
    ):
        super(BookSpider, self).__init__(*args, **kwargs)
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
        if response.url != self.login_url:
            self.is_login = True
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        book = Selector(response)
        if self.is_login:
            item = AccountItem()
            for sel in book.xpath(
                    '//*[@id="mylib_content"]/table/tr')[1:8]:
                barcode = sel.xpath('td/text()').extract()[0]
                title = sel.xpath('td/a/text()').extract()[0]
                author = sel.xpath('td/text()').extract()[1]
                data = sel.xpath('td/text()').extract()[2]
                backdata = sel.xpath(
                    'td/font/text()').extract()[0].rstrip()
                self.books[barcode] = \
                    {
                        'title': title,
                        'author': author,
                        'data': data,
                        'backdata': backdata
                    }
                item['books'] = self.books
            item['name'] = response.xpath('//*[@id="menu"]/div/text()').extract()
            item['number'] = self.number
            item['passwd'] = self.passwd

        yield item
