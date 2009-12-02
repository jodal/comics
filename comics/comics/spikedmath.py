from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Spiked Math'
    language = 'en'
    url = 'http://www.spikedmath.com/'
    start_date = '2009-08-24'
    history_capable_days = 20
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Mike, CC BY-NC-SA 2.5'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/SpikedMath')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('div.asset-body img')
            title = entry.title
            return CrawlerResult(url, title)
