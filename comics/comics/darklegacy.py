from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Dark Legacy'
    language = 'en'
    url = 'http://www.darklegacycomics.com/'
    start_date = '2006-01-01'
    rights = 'Arad Kedar'

class Crawler(CrawlerBase):
    history_capable_date = '2006-12-09'
    schedule = 'Su'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.darklegacycomics.com/feed.xml')
        for entry in feed.for_date(pub_date):
            title = entry.title
            url = entry.link.replace('.html', '.jpg')
            return CrawlerResult(url)
