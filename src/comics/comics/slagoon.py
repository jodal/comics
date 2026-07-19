import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sherman's Lagoon"
    language = "en"
    url = "https://shermanslagoon.com"
    start_date = "1991-05-13"
    rights = "Jim Toomey"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2003-12-29"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("shermanslagoon", pub_date)
