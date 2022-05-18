from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dustin"
    language = "en"
    url = "https://www.comicskingdom.com/dustin"
    start_date = "2010-01-04"
    rights = "Steve Kelley & Jeff Parker"


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_date = "2010-01-04"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("dustin", pub_date)
