from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Bestis"
    language = "no"
    url = "https://www.dagbladet.no/tegneserie/bestis/"
    rights = "Kenneth Larsen"
    active = False


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 30
    schedule = "Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("bestis", pub_date)
