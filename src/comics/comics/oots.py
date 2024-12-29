from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Order of the Stick"
    language = "en"
    url = "http://www.giantitp.com/"
    start_date = "2003-09-30"
    rights = "Rich Burlew"


class Crawler(CrawlerBase):
    history_capable_days = 10
    time_zone = "America/New_York"
    headers = {"User-Agent": "Mozilla/5.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.giantitp.com/comics/oots.rss")
        if len(feed.all()):
            entry = feed.all()[0]
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/comics/oots/"]')
            title = entry.title
            return CrawlerImage(url, title)
