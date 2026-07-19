import datetime as dt

from comics.aggregator.crawler import CrawlerResult, GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Non Sequitur"
    language = "en"
    url = "https://www.gocomics.com/nonsequitur"
    start_date = "1992-02-16"
    rights = "Wiley Miller"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1992-02-16"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        return self.crawl_helper("nonsequitur", pub_date)
