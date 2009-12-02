from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Hark, A Vagrant!'
    language = 'en'
    url = 'http://www.harkavagrant.com/'
    start_date = '2008-05-01'
    history_capable_days = 120
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Kate Beaton'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/vagrant.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/history/"]')
            title = entry.summary.title('img[src*="/history/"]')
            return CrawlerResult(url, title)
