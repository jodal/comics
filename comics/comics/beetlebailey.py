from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Beetle Bailey"
    language = "en"
    url = "https://www.comicskingdom.com/beetle-bailey-1"
    start_date = "1950-01-01"
    rights = "Mort Walker"


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_date = "1998-10-05"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("beetle-bailey-1", pub_date)
