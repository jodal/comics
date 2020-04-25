from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Order of the Stick"
    language = "en"
    url = "http://www.giantitp.com/"
    start_date = "2003-09-30"
    rights = "Rich Burlew"


class Crawler(CrawlerBase):
    history_capable_days = 1
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.giantitp.com/comics/oots.rss")
        if len(feed.all()):
            entry = feed.all()[0]
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/comics/images/"]')
            title = entry.title
            return CrawlerImage(url, title)
