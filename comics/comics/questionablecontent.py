from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Questionable Content'
    language = 'en'
    url = 'http://questionablecontent.net/'
    start_date = '2003-08-01'
    history_capable_date = '2003-08-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6
    rights = 'Jeph Jacques'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.questionablecontent.net/QCRSS.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            return CrawlerResult(url, title)
