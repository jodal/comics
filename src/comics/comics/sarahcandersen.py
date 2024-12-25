from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sarah's Scribbles"
    language = "en"
    url = "http://www.sarahcandersen.com/"
    start_date = "2011-01-01"
    rights = "Sarah Andersen"


class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = "We,Sa"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://sarahcandersen.com/rss")
        for entry in feed.for_date(pub_date):
            urls = entry.summary.src('img[src*="_500"]', allow_multiple=True)
            return [CrawlerImage(url) for url in urls]
