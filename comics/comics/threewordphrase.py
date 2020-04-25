from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Three Word Phrase"
    language = "en"
    url = "http://www.threewordphrase.com/"
    start_date = "2010-07-13"
    end_date = "2014-05-27"
    rights = "Ryan Pequin"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
