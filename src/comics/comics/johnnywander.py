from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Johnny Wander"
    language = "en"
    url = "http://www.johnnywander.com/"
    start_date = "2008-09-30"
    rights = "Yuko Ota & Ananth Panagariya"


class Crawler(CrawlerBase):
    history_capable_days = 40
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.johnnywander.com/feed")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            text = entry.summary.title("img")
            return CrawlerImage(url, title, text)
