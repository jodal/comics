from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Bug'
    language = 'en'
    url = 'http://www.bugcomic.com/'
    start_date = '2009-10-19'
    rights = 'Adam Huber'


class Crawler(CrawlerBase):
    history_capable_days = 15
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'US/Mountain'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.bugcomic.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[class="comicthumbnail"]')
            title = entry.title
            if url is None:
                return
            return CrawlerImage(url, title)
