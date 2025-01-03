from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Misfile"
    language = "en"
    url = "http://www.misfile.com/"
    start_date = "2004-03-01"
    rights = "Chris Hazelton"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 10
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper(ComicData.url, pub_date)
