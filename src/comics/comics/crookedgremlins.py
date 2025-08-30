from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Crooked Gremlins"
    language = "en"
    url = "http://www.crookedgremlins.com/"
    start_date = "2008-04-01"
    end_date = "2015-07-28"
    rights = "Carter Fort and Paul Lucci"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
