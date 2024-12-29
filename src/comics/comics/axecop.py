from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Axe Cop"
    language = "en"
    url = "http://www.axecop.com/"
    start_date = "2010-01-02"
    rights = "Ethan Nicolle"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = "America/Los_Angeles"

    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://axecop.com/feed/")
        for entry in feed.for_date(pub_date):
            title = entry.title
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if url is None:
                continue
            url = url.replace("-150x150", "")
            return CrawlerImage(url, title)
