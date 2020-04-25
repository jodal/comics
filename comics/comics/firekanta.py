# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Firekanta"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/firekanta"
    rights = "Nils Axle Kanten"


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 14
    schedule = "Mo,We,Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("firekanta", pub_date)
