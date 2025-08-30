from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Daryl Cagle's Political Blog"
    language = "en"
    url = "http://www.cagle.com/"
    start_date = "2001-01-04"
    rights = "Daryl Cagle"


class Crawler(CrawlerBase):
    history_capable_days = 365
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://cagle.com/daryl-cagle/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            return CrawlerImage(url, title)
