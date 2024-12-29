from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nedroid"
    language = "en"
    url = "http://www.nedroid.com/"
    start_date = "2006-04-24"
    rights = "Anthony Clark"


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = "America/New_York"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://nedroid.com/feed/")
        for entry in feed.for_date(pub_date):
            if "Comic" not in entry.tags:
                continue
            page = self.parse_page(entry.link)
            url = page.src("#comic img")
            title = entry.title
            text = page.title("#comic img")
            return CrawlerImage(url, title, text)
