import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Cyanide and Happiness"
    language = "en"
    url = "https://explosm.net/comics"
    start_date = "2005-01-26"
    rights = "Kris Wilson, Rob DenBleyker, Matt Melvin, & Dave McElfatrick "


class Crawler(CrawlerBase):
    history_length_days = 14
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("https://explosm.net/rss.xml")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            # The comic is the first image on the image server
            urls = page.srcs('img[src*="static.explosm.net"]')
            if not urls:
                continue
            return CrawlerImage(urls[0], entry.title)
        return None
