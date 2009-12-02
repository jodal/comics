from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Unspeakable Vault (of Doom)'
    language = 'en'
    url = 'http://www.macguff.fr/goomi/unspeakable/'
    history_capable_days = 180
    time_zone = 1
    rights = 'Francois Launet'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.macguff.fr/goomi/unspeakable/rss.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Strip #'):
                url = entry.content0.src('img')
                title = entry.summary.text('')
                return CrawlerResult(url, title)
