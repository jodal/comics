from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Girls With Slingshots"
    language = "en"
    url = "http://www.girlswithslingshots.com/"
    start_date = "2004-09-30"
    rights = "Danielle Corsetto"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 30
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper(ComicData.url, pub_date)
