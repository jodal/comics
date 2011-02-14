from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase
from comics.core.models import Release

class Meta(MetaBase):
    name = 'The Gutters'
    language = 'en'
    url = 'http://the-gutters.com/'
    rights = 'Blind Ferret Entertainment'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,We,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/TheGutters')
        for entry in feed.for_date(pub_date):
            url = entry.html(entry.description).src('img[src*="/comics/"]')
            title = entry.title.replace('Gutters: ', '')
            return CrawlerImage(url, title)
