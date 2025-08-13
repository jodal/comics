import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Pole Dancing Adventures"
    language = "en"
    url = "http://poledancingadventures.com/"
    start_date = "2010-01-28"
    rights = "Leen Isabel"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2018-05-29"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://poledancingadventures.com/category/comics/feed")
        for entry in feed.for_date(pub_date):
            results = [
                CrawlerImage(url)
                for url in entry.content0.srcs("img")
                # Look for NNN-*.jpg to differentiate comics from other images
                if re.match(r".*\/\d\d\d-.*\.jpg", url) is not None
            ]
            if results:
                results[0].title = entry.title
                return results
