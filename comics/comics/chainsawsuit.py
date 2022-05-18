from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "chainsawsuit"
    language = "en"
    url = "http://chainsawsuit.com/"
    start_date = "2008-03-12"
    rights = "Kris Straub"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        pass
