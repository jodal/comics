from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Adventures of Business Cat"
    language = "en"
    url = "http://www.businesscat.happyjar.com/"
    start_date = "2014-01-07"
    rights = "Tom Fonder"


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = "Europe/London"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.businesscat.happyjar.com/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if not url:
                continue
            url = url.replace("-170x170", "")
            title = entry.title
            return CrawlerImage(url, title)
