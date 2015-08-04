# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import FormRequest, Request  # noqa
from scrapy.selector import Selector
from LibCrawler.items import LibcrawlerItem


class LibSpider(scrapy.Spider):

    name = 'lib'
    allowed_domains = [
        'http://lib.sdut.edu.cn/index.html'
    ]
    login_url = 'http://222.206.65.12/reader/redr_verify.php'
    start_urls = [
        'http://222.206.65.12/reader/book_lst.php'
    ]

    download_delay = 0.5
    is_login = False

    def __init__(
        self,
        number='13110581135',
        passwd='13110581135',
        select='cert_no',
        *args, **kwargs
    ):
        super(LibSpider, self).__init__(*args, **kwargs)
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
            callback=self.after_login
        )]

    def after_login(self, response):
        if re.search(r'注销', response.body):
            self.is_login = True
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        book = Selector(response)
        if self.is_login:
            for sel in book.xpath('//*[@id="mylib_content"]/table/tr')[1:8]:
                item = LibcrawlerItem()
                item['barcode'] = sel.xpath('td/text()').extract()[0]
                item['title'] = sel.xpath('td/a/text()').extract()[0]
                item['author'] = sel.xpath('td/text()').extract()[1]
                item['data'] = sel.xpath('td/text()').extract()[2]
                item['backdata'] = sel.xpath(
                    'td/font/text()').extract()[0].rstrip()
                yield item
