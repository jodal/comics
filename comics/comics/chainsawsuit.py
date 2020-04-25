from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "chainsawsuit"
    language = "en"
    url = "http://chainsawsuit.com/"
    start_date = "2008-03-12"
    rights = "Kris Straub"


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://chainsawsuit.com/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
