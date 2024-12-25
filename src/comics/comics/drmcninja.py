from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Adventures of Dr. McNinja"
    language = "en"
    url = "http://drmcninja.com/"
    start_date = "2004-08-03"
    rights = "Christopher Hastings"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = "Mo,We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://drmcninja.com/feed")
        for entry in feed.for_date(pub_date):
            if "/comic/" not in entry.link:
                continue
            page = self.parse_page(entry.link)
            url = page.src("#comic img")
            title = entry.title
            text = page.title("#comic img")
            return CrawlerImage(url, title, text)
