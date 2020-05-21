from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Blaster Nation"
    language = "en"
    url = "http://www.blasternation.com/"
    start_date = "2011-01-27"
    rights = "Leslie Brown & Brad Brown"
    active = False


class Crawler(CrawlerBase):
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        pass
