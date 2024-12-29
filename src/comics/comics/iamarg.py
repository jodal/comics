from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "I AM ARG!"
    language = "en"
    url = "http://iamarg.com/"
    start_date = "2011-05-08"
    rights = "Andrew Gregoire"


class Crawler(CrawlerBase):
    history_capable_days = 100
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://iamarg.com/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics-rss/"]')
            if not url:
                continue
            url = url.replace("comics-rss", "comics")
            title = entry.title
            return CrawlerImage(url, title)
