from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Chopping Block"
    language = "en"
    url = "http://choppingblock.keenspot.com/"
    start_date = "2000-07-25"
    end_date = "2012-08-22"
    active = False
    rights = "Lee Adam Herold"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
