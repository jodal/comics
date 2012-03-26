from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Manala Next Door'
    language = 'en'
    url = 'http://www.manalanextdoor.com/'
    start_date = '2011-01-23'
    rights = 'Humon'

class Crawler(CrawlerBase):
    time_zone = 0

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/manalanextdoor')
        for entry in feed.all():
            url = entry.summary.src('img[src*="/art/"]')
            if url is not None:
                url = url.replace('/thumb', '')
            title = entry.title
            return CrawlerImage(url, title)
