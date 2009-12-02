from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Looking For Group'
    language = 'en'
    url = 'http://lfgcomic.com/'
    start_date = '2006-11-06'
    history_capable_date = '2006-11-06'
    schedule = 'Mo,Th'
    time_zone = -5
    rights = 'Ryan Sohmer & Lar deSouza'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/LookingForGroup')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="lfgcomic.com"]')
            title = entry.title.replace('Looking For Group:', '').strip()
            return CrawlerResult(url, title)
