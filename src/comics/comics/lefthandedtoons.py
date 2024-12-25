from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Left-Handed Toons"
    language = "en"
    url = "http://www.lefthandedtoons.com/"
    start_date = "2007-01-14"
    rights = "Justin & Drew"


class Crawler(CrawlerBase):
    history_capable_days = 12
    schedule = "Mo,Tu,We,Th"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/lefthandedtoons/awesome")

        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/toons/"]')
            title = entry.title

            if url:
                return CrawlerImage(url, title)
