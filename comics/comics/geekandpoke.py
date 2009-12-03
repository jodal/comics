from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Geek and Poke'
    language = 'en'
    url = 'http://www.geekandpoke.com/'
    start_date = '2006-08-22'
    rights = 'Oliver Widder, CC BY-ND 2.0'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://geekandpoke.typepad.com/geekandpoke/atom.xml')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img.asset-image')
            title = entry.title
            return CrawlerResult(url, title)
