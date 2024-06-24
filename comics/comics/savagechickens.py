from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Savage Chickens"
    language = "en"
    url = "http://www.savagechickens.com/"
    start_date = "2005-01-31"
    rights = "Dave Savage"


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.savagechickens.com/feed")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/"]')
            title = entry.title
            return CrawlerImage(url, title)
