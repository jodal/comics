from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dinosaur Comics"
    language = "en"
    url = "http://www.qwantz.com/"
    start_date = "2003-02-01"
    rights = "Ryan North"


class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = "Mo,Tu,We,Th"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.rsspect.com/rss/qwantz.xml")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.title('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
