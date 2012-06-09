from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Abstruse Goose'
    language = 'en'
    url = 'http://www.abstrusegoose.com/'
    start_date = '2008-02-01'
    rights = 'lcfr, CC BY-NC 3.0 US'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Th'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://abstrusegoose.com/feed/atom')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/strips/"]')
            title = entry.title
            text = entry.content0.title('img[src*="/strips/"]')
            return CrawlerImage(url, title, text)
