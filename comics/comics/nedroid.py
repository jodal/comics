from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Nedroid'
    language = 'en'
    url = 'http://www.nedroid.com/'
    start_date = '2006-04-24'
    rights = 'Anthony Clark'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://nedroid.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comic' in entry.tags:
                title = entry.title
                url = entry.summary.src('img')
                text = entry.summary.title('img')
                return CrawlerResult(url, title, text)
