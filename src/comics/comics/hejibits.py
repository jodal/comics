from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hejibits"
    language = "en"
    url = "https://www.hejibits.com/"
    start_date = "2010-03-02"
    rights = "John Kleckner"


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://hejibits.com/rss")
        for entry in feed.for_date(pub_date):
            if "comic" not in entry.tags:
                continue
            results = [CrawlerImage(url) for url in entry.summary.srcs("img")]
            if results:
                results[0].title = entry.title
                return results
