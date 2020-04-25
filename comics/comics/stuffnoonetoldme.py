from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Stuff No One Told Me"
    language = "en"
    url = "http://stuffnoonetoldme.blogspot.com/"
    start_date = "2010-05-31"
    end_date = "2011-10-18"
    active = False
    rights = "Alex Noriega"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
