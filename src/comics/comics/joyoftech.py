import datetime as dt
import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Joy of Tech"
    language = "en"
    url = "http://www.geekculture.com/joyoftech/"
    start_date = "2000-08-14"
    rights = "Geek Culture"


class Crawler(CrawlerBase):
    history_length_days = 30
    schedule = "Mo,Th"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://www.joyoftech.com/joyoftech/jotblog/atom.xml")
        for entry in feed.for_date(pub_date):
            title = entry.title

            matches = re.search(r"joyarchives/(\d+)\.html", str(entry.link))
            if matches is None:
                continue
            num = matches.group(1)

            page = self.parse_page(entry.link)
            # Some pages also hold a thumbnail beside the comic
            url = page.src(f'img[src="/joyoftech/joyimages/{num}.png"]', first=True)
            if url is None:
                url = page.src(f'img[src*="/joyimages/{num}."]', first=True)
            if url is None:
                continue
            return CrawlerImage(url, title)
        return None
