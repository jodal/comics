from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "F@NB0Y$"
    language = "en"
    url = "http://www.fanboys-online.com/"
    start_date = "2006-04-19"
    rights = "Scott Dewitt"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass
