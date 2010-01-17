from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Zits'
    language = 'en'
    url = 'http://www.arcamax.com/zits'
    start_date = '1997-07-01'
    rights = 'Jerry Scott and Jim Borgman'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Tu,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.arcamax.com/zits/channelfeed')
        for entry in feed.all():
            if entry.title.endswith(pub_date.strftime('%-1m/%-1d/%Y')):
                page = self.parse_page(entry.link)
                url = page.src('p.m0 img')
                return CrawlerImage(url)
