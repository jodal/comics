from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'LO-KU'
    language = 'en'
    url = 'http://www.lo-ku.com/'
    start_date = '2009-06-15'
    rights = 'Thomas & Daniel Drinnen'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Tu'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.lo-ku.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/comics/"]')
            url = url.replace('/thumbs', '').replace('-medium', '')
            title = entry.title
            return CrawlerImage(url, title)
