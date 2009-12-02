from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Zits'
    language = 'en'
    url = 'http://www.arcamax.com/zits'
    start_date = '1997-07-01'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Tu,Fr,Sa,Su'
    time_zone = -5
    rights = 'Jerry Scott and Jim Borgman'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.arcamax.com/zits/channelfeed')
        for entry in feed.all():
            if entry.title.endswith(pub_date.strftime('%-1m/%-1d/%Y')):
                page = self.parse_page(entry.link)
                url = page.src('p.m0 img')
                return CrawlerResult(url)
