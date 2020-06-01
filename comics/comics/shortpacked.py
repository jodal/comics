from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Shortpacked"
    language = "en"
    url = "http://www.shortpacked.com/"
    start_date = "2005-01-17"
    rights = "David Willis"


class Crawler(ComicControlCrawlerBase):
    schedule = "Mo,We,Fr"
    history_capable_days = 32
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("https://www.shortpacked.com", pub_date)
