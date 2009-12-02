from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Basic Instructions'
    language = 'en'
    url = 'http://www.basicinstructions.net/'
    start_date = '2006-07-01'
    history_capable_days = 100
    schedule = 'We,Su'
    time_zone = -7
    rights = 'Scott Meyer'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.basicinstructions.net/atom.xml')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/comics/"]', False)
            title = entry.title
            return CrawlerResult(url, title)
