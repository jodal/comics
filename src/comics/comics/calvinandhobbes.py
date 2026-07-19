import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Calvin and Hobbes"
    language = "en"
    url = "https://www.gocomics.com/calvinandhobbes"
    start_date = "1985-11-18"
    end_date = "1995-12-31"
    rights = "Bill Watterson"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1985-11-18"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("calvinandhobbes", pub_date)
