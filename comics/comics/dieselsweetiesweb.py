from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Diesel Sweeties (web)"
    language = "en"
    url = "http://www.dieselsweeties.com/"
    start_date = "2000-01-01"
    rights = "Richard Stevens"


class Crawler(CrawlerBase):
    history_capable_date = "2000-01-01"
    schedule = "Mo,We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.dieselsweeties.com/ds-unifeed.xml")
        for entry in feed.for_date(pub_date):
            if not hasattr(entry, "summary"):
                continue
            url = entry.summary.src('img[src*="/strips666/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/strips666/"]')
            return CrawlerImage(url, title, text)
