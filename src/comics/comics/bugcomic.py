from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Bug Martini"
    language = "en"
    url = "http://www.bugmartini.com/"
    start_date = "2009-10-19"
    rights = "Adam Huber"


class Crawler(CrawlerBase):
    history_capable_days = 15
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "US/Mountain"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.bugmartini.com/feed/")
        for entry in feed.for_date(pub_date):
            title = entry.title
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if url:
                url = url.replace("?resize=520%2C280", "")
            return CrawlerImage(url, title)
