from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Darths & Droids"
    language = "en"
    url = "http://darthsanddroids.net/"
    start_date = "2007-09-14"
    rights = "The Comic Irregulars"


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = "Tu,Th,Su"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://darthsanddroids.net/rss.xml")
        for entry in feed.for_date(pub_date):
            if entry.title.startswith("Episode"):
                url = entry.summary.src("img")
                title = entry.title
                return CrawlerImage(url, title)
