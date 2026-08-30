import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Order of the Stick"
    language = "en"
    url = "https://www.giantitp.com/"
    start_date = "2003-09-30"
    rights = "Rich Burlew"


class Crawler(CrawlerBase):
    history_length_days = 10
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://www.giantitp.com/comics/oots.rss")
        if len(feed.all()):
            entry = feed.all()[0]
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/comics/oots/"]')
            title = entry.title
            return CrawlerImage(url, title)
        return None
