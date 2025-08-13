from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Samtull"
    language = "no"
    url = "https://nettserier.no/aikomi/comic/"
    rights = "Emil Åslund"
    start_date = "2015-01-24"


class Crawler(NettserierCrawlerBase):
    history_capable_date = "2015-01-24"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        return self.crawl_helper(1815, pub_date)
