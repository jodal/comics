from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Diesel Sweeties (web)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2000-01-01'
    rights = 'Richard Stevens'

class Crawler(CrawlerBase):
    history_capable_date = '2000-01-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.dieselsweeties.com/ds-unifeed.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('DS Web:'):
                url = entry.summary.src('img')
                title = entry.title.replace('DS Web: ', '').strip()
                text = entry.summary.alt('img')
                return CrawlerResult(url, title, text)
