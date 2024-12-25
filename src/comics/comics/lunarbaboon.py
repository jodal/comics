from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lunarbaboon"
    language = "en"
    url = "http://www.lunarbaboon.com/"
    start_date = "2012-07-09"
    rights = "Lunarbaboon"


class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.lunarbaboon.com/comics/rss.xml")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            return CrawlerImage(url, title)
