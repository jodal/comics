from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Mary Death"
    language = "en"
    url = "http://www.marydeathcomics.com/"
    start_date = "2013-01-17"
    rights = "Matthew Tarpley, CC BY-NC 3.0"


class Crawler(CrawlerBase):
    history_capable_days = 365
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.marydeathcomics.com/feed")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if not url:
                continue
            url = url.replace("-150x150", "")
            title = entry.title
            return CrawlerImage(url, title)
