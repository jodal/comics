from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Veslemøy"
    language = "no"
    url = "http://www.side2.no/tegneserie/veslemoy/"
    start_date = "2008-11-14"
    end_date = "2012-12-31"
    active = False
    rights = "Vantina Nina Andreassen"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
