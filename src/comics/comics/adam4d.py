from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Adam4d.com"
    language = "en"
    url = "http://www.adam4d.com/"
    start_date = "2012-07-03"
    rights = "Adam Ford"


class Crawler(CrawlerBase):
    history_capable_days = 10
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://adam4d.com/feed/")
        for entry in feed.for_date(pub_date):
            urls = [
                url.replace("comics-rss", "comics")
                for url in entry.content0.srcs('img[src*="/wp-content/"]')
            ]
            results = [CrawlerImage(url) for url in urls]
            if not results:
                continue
            results[0].title = entry.title
            return results
