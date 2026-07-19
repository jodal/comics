import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Peanuts"
    language = "en"
    url = "https://www.gocomics.com/peanuts"
    start_date = "1950-10-02"
    end_date = "2000-02-13"
    rights = "Charles M. Schulz"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1950-10-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("peanuts", pub_date)
