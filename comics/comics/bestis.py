# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Bestis"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/bestis/"
    rights = "Kenneth Larsen"


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 14
    schedule = "Mo,Tu,We,Th,Fr,Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("bestis", pub_date)
