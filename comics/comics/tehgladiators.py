from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Teh Gladiators"
    language = "en"
    url = "http://www.tehgladiators.com/"
    start_date = "2008-03-18"
    rights = "Uros Jojic & Borislav Grabovic"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = "We"
    time_zone = "Europe/Belgrade"

    def crawl(self, pub_date):
        pass
