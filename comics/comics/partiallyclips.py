from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'PartiallyClips'
    language = 'en'
    url = 'http://partiallyclips.com/'
    start_date = '2002-01-01'
    rights = 'Robert T. Balder'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Tu'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://partiallyclips.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title.split(' - ')[0]
            return CrawlerImage(url, title)
