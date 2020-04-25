from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Something of that Ilk"
    language = "en"
    url = "http://www.somethingofthatilk.com/"
    start_date = "2011-02-19"
    end_date = "2013-11-06"
    active = False
    rights = "Ty Devries"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
