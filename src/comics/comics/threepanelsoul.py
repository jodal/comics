from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Three Panel Soul"
    language = "en"
    url = "http://www.threepanelsoul.com/"
    start_date = "2006-11-05"
    rights = "Ian McConville & Matt Boyd"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 180
    schedule = "Mo"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper(ComicData.url, pub_date)
