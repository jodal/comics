from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Poorly Drawn Lines"
    language = "en"
    url = "http://poorlydrawnlines.com/"
    start_date = "2011-04-18"
    rights = "Reza Farazmand, CC BY-NC 3.0"


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/PoorlyDrawnLines")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
