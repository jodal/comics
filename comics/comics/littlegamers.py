from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Little Gamers"
    language = "en"
    url = "https://www.little-gamers.com/"
    start_date = "2000-12-01"
    rights = "Christian Fundin & Pontus Madsen"


class Crawler(CrawlerBase):
    history_capable_date = "2000-12-01"
    time_zone = "Europe/Stockholm"

    def crawl(self, pub_date):
        url = "https://www.little-gamers.com/comics/%s.jpg" % pub_date.strftime(
            "%Y-%m-%d"
        )
        return CrawlerImage(url)
