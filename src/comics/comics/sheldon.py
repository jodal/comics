from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sheldon"
    language = "en"
    url = "https://www.sheldoncomics.com/"
    start_date = "2001-11-30"
    rights = "Dave Kellett"


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://www.sheldoncomics.com/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/uploads/"]')
            return CrawlerImage(url)
