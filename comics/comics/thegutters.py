import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Gutters"
    language = "en"
    url = "http://the-gutters.com/"
    rights = "Blind Ferret Entertainment"


class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = "Tu,Fr"
    time_zone = "America/Montreal"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/TheGutters")
        for entry in feed.for_date(pub_date):
            title = entry.title
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if not url:
                continue
            url = re.sub(r"-\d+x\d+.jpg", ".jpg", url)
            return CrawlerImage(url, title)
