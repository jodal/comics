from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Free Range"
    language = "en"
    url = "https://www.gocomics.com/freerange"
    rights = "Bill Whitehead"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2007-02-03"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("freerange", pub_date)
