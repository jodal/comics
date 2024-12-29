from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Mutts"
    language = "en"
    url = "http://www.mutts.com"
    start_date = "1994-01-01"
    rights = "Patrick McDonnell"


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_date = "1994-09-11"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("mutts", pub_date)
