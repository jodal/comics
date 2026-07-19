import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Not Invented Here (gocomics.com)"
    language = "en"
    url = "https://www.gocomics.com/not-invented-here"
    start_date = "2009-09-21"
    rights = "Bill Barnes and friends"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2015-12-28"
    schedule = "Mo,Tu,We,Th"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("not-invented-here", pub_date)
