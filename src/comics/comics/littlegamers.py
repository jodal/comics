from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Little Gamers"
    language = "en"
    url = "https://www.little-gamers.com/"
    start_date = "2000-12-01"
    end_date = "2025-02-05"
    rights = "Christian Fundin & Pontus Madsen"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
