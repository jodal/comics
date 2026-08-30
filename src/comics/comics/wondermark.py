import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Wondermark"
    language = "en"
    url = "http://wondermark.com/"
    start_date = "2003-04-25"
    rights = "David Malki"


class Crawler(CrawlerBase):
    history_length_days = 28
    schedule = "Tu,We,Th,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed_url = "http://feeds.feedburner.com/wondermark"
        feed = self.parse_feed(feed_url)
        for entry in feed.for_date(pub_date):
            if "Comic" not in entry.tags:
                continue
            selector = 'img[src*="/wp-content/uploads/"]'
            url = entry.content0.src(selector)
            if url is None:
                continue
            title = entry.title
            text = entry.content0.alt(selector)
            return CrawlerImage(url, title, text)
        return None
