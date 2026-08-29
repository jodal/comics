import datetime as dt
import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Oatmeal"
    language = "en"
    url = "http://theoatmeal.com/"
    rights = "Matthew Inman"


class Crawler(CrawlerBase):
    history_length_days = 90
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://feeds.feedburner.com/oatmealfeed")
        for entry in feed.for_date(pub_date):
            # The feed also holds blog posts, which are not comics
            match = re.search(r"/comics/([^/?]+)", str(entry.link))
            if match is None:
                continue
            page = self.parse_page(entry.link)
            selector = f'img[src*="/comics/{match.group(1)}/"]'
            results = [CrawlerImage(url) for url in page.srcs(selector)]
            if results:
                results[0].title = entry.title
                return results
        return None
