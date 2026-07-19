import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Pickles"
    language = "en"
    url = "https://www.gocomics.com/pickles"
    start_date = "2003-10-01"
    rights = "Brian Crane"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2003-10-01"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("pickles", pub_date)
