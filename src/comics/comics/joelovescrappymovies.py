from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Joe Loves Crappy Movies"
    language = "en"
    url = "https://www.digitalpimponline.com/comic/movie/"
    start_date = "2005-04-04"
    end_date = "2019-03-14"
    rights = "Joseph Dunn"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
