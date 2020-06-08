# encoding: utf-8

from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ménage à 3"
    language = "en"
    url = "http://www.ma3comic.com/"
    start_date = "2008-05-17"
    rights = "Giz & Dave Zero 1"
    active = False


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 50
    schedule = "Tu,Th,Sa"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper(
            "https://pixietrixcomix.com/menage-a-3", pub_date
        )
