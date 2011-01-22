from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Romantically Apocalyptic'
    language = 'en'
    url = 'http://www.romanticallyapocalyptic.com/'
    rights = 'Vitaly S. Alexius'

class Crawler(CrawlerBase):
    history_capable_days = 365
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.romanticallyapocalyptic.com/'
            'feeds/comic/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            return CrawlerImage(url, title)
