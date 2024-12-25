from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "ExtraLife"
    language = "en"
    url = "http://www.myextralife.com/"
    start_date = "2001-06-17"
    rights = "Scott Johnson"


class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = "Mo"
    time_zone = "US/Mountain"

    # Without User-Agent set, the server returns empty responses
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.myextralife.com/category/comic/feed/")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/"]')
            title = entry.title
            return CrawlerImage(url, title)
