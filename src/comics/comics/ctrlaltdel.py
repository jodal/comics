import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Ctrl+Alt+Del"
    language = "en"
    url = "https://cad-comic.com/category/ctrl-alt-del/"
    start_date = "2002-10-23"
    rights = "Tim Buckley"


class Crawler(CrawlerBase):
    history_length_days = 20
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        # The site feed holds only the newest posts, which are another comic
        feed = self.parse_feed("https://cad-comic.com/category/ctrl-alt-del/feed/")

        for entry in feed.for_date(pub_date):
            if "Ctrl Alt Del" not in entry.tags:
                continue
            page = self.parse_page(entry.link)
            url = page.src(".comicpage img")
            title = entry.title
            return CrawlerImage(url, title)
        return None
