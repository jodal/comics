from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "you and me and cats"
    language = "en"
    url = "http://strawberry-pie.net/SA/"
    start_date = "2009-07-01"
    rights = "bubble"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 365
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        pass
