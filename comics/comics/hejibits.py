from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hejibits'
    language = 'en'
    url = 'http://www.hejibits.com/'
    start_date = '2010-03-02'
    rights = 'John Kleckner'


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'Mo'
    time_zone = 'US/Pacific'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.hejibits.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
