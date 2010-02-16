from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Calamities of Nature'
    language = 'en'
    url = 'http://www.calamitiesofnature.com/'
    start_date = '2007-12-11'
    rights = 'Tony Piro'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -9

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/calamitiesofnature')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Blog'):
                continue
            url = entry.summary.src('img[src*="/archive/"]')
            if url is not None:
                url = url.replace('_sm', '')
            title = entry.title.split(' - ')[-1]
            return CrawlerImage(url, title)
