from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Jesus & Mo"
    language = "en"
    url = "http://www.jesusandmo.net/"
    start_date = "2005-11-24"
    rights = "Mohammed Jones, CC BY-NC-SA 3.0"


class Crawler(CrawlerBase):
    history_capable_date = "2005-11-24"
    schedule = "We"
    time_zone = "Europe/London"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://www.jesusandmo.net/comic/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src("img[src*='/uploads/']")
            if not url:
                continue
            return CrawlerImage(url, entry.title)
