from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Calamities of Nature"
    language = "en"
    url = "http://www.calamitiesofnature.com/"
    active = False
    start_date = "2007-12-11"
    end_date = "2012-03-12"
    rights = "Tony Piro"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
