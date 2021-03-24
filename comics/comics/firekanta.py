from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Firekanta"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/firekanta"
    rights = "Nils Axle Kanten"
    active = False


class Crawler(DagbladetCrawlerBase):
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("firekanta", pub_date)
