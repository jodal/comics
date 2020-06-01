from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sticky Dilly Buns"
    language = "en"
    url = "http://www.stickydillybuns.com/"
    start_date = "2013-01-07"
    rights = "G. Lagace"
    active = False


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 50
    schedule = "Mo,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper(
            "https://pixietrixcomix.com/sticky-dilly-buns", pub_date
        )
