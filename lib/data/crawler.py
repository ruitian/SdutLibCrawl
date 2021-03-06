from billiard import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging  # noqa

settings = get_project_settings()


class Crawler():
    def __init__(self):
        self.crawler = CrawlerProcess(settings)


class VarifyCrawler(Crawler):

    def _crawl(self, number, passwd):
        self.crawler.crawl(
            'varify',
            number=number,
            passwd=passwd
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, number, passwd):
        p = Process(
            target=self._crawl,
            args=[
                number,
                passwd
            ]
        )
        p.start()
        p.join()


class BooksCrawler(Crawler):

    def _crawl(self, number, passwd):
        self.crawler.crawl(
            'books',
            number=number,
            passwd=passwd
        )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, number, passwd):
        p = Process(
            target=self._crawl,
            args=[
                number,
                passwd
            ]
        )
        p.start()
        p.join()
