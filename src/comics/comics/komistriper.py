from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Samtull"
    language = "no"
    url = "https://nettserier.no/aikomi/comic/"
    active = False
    start_date = "2015-01-24"
    end_date = "2022-11-21"
    rights = "Emil Åslund"


class Crawler(NettserierCrawlerBase):
    history_capable_date = "2015-01-24"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass  # Comic no longer published
