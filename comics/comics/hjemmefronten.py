# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Intet nytt fra hjemmefronten"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/intetnyttfrahjemmefronten/"
    rights = "Therese G. Eide"


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 30
    schedule = "Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("intetnyttfrahjemmefronten", pub_date)
