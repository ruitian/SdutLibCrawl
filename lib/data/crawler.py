from billiard import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging  # noqa

settings = get_project_settings()


class Crawler():
    def __init__(self):
        self.crawler = CrawlerProcess(settings)


class AccountCrawler(Crawler):

    def _crawl(self, username, password):
        self.crawler.crawl(
            'lib',
            username=username,
            password=password
            )
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, username, password):
        p = Process(
            target=self._crawl,
            args=[
                username,
                password
            ]
        )
        p.start()
        p.join()
