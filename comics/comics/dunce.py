from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dunce"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/dunce"
    rights = "Jens K. Styve"


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 30  # 3 saturdays
    schedule = "Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper("dunce", pub_date)
