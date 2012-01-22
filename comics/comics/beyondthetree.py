from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Beyond the Tree'
    language = 'en'
    url = 'http://beyondthetree.wordpress.com/'
    start_date = '2008-03-20'
    rights = 'Nhani'

class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = 'Th,Su'
    time_zone = 0

    def crawl(self, pub_date):
        feed = self.parse_feed('http://beyondthetree.wordpress.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comic' not in entry.tags:
                continue
            url = entry.content0.src('img[src*="/btt-"]')
            title = entry.title
            return CrawlerImage(url, title)
