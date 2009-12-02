from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'A Softer World'
    language = 'en'
    url = 'http://www.asofterworld.com/'
    start_date = '2003-02-07'
    history_capable_date = '2003-02-07'
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Joey Comeau, Emily Horne'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/asw.xml')
        for entry in feed.for_date(pub_date):
            if entry.link != 'http://www.asofterworld.com':
                url = entry.summary.src('img[src*="/clean/"]')
                title = entry.title
                text = entry.summary.title('img[src*="/clean/"]')
                return CrawlerResult(url, title, text)
