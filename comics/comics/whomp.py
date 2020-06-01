from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Whomp!"
    language = "en"
    url = "http://www.whompcomic.com/"
    start_date = "2010-06-14"
    rights = "Ronnie Filyaw"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 70
    schedule = "We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("http://www.whompcomic.com", pub_date)
