from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Critical miss"
    language = "en"
    url = (
        "http://www.escapistmagazine.com"
        "/articles/view/comicsandcosplay/comics/critical-miss"
    )
    start_date = "2010-05-18"
    rights = "Cory Rydell & Grey Carter"
    active = False


class Crawler(CrawlerBase):
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        pass
