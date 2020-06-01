from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Goblins"
    language = "en"
    url = "http://www.goblinscomic.com/"
    start_date = "2005-05-29"
    rights = "Tarol Hunt"


class Crawler(ComicControlCrawlerBase):
    history_capable_days = 30
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        return self.crawl_helper("http://www.goblinscomic.com", pub_date)
