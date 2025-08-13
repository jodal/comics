from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Red Meat"
    language = "en"
    url = "http://www.redmeat.com/"
    active = False
    start_date = "1996-06-10"
    rights = "Max Cannon"


class Crawler(CrawlerBase):
    schedule = "Tu"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        pass  # Comic no longer published
