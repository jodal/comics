from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Goblins'
    language = 'en'
    url = 'http://www.goblinscomic.com/'
    start_date = '2005-05-29'
    rights = 'Tarol Hunt'


class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.goblinscomic.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            url = entry.summary.src('img[src*="/comics/"]')
            return CrawlerImage(url)
