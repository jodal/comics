from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "CommitStrip"
    language = "en"
    url = "http://www.commitstrip.com/en/"
    start_date = "2012-02-22"
    rights = "Etienne Issartial"


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.commitstrip.com/en/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
