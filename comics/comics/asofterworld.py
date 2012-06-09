import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'A Softer World'
    language = 'en'
    url = 'http://www.asofterworld.com/'
    start_date = '2003-02-07'
    rights = 'Joey Comeau, Emily Horne'

class Crawler(CrawlerBase):
    history_capable_date = '2003-02-07'
    schedule = None
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/asw.xml')
        for entry in feed.for_date(pub_date):
            if entry.title == 'A Softer World':
                urls = entry.summary.src('img[src*="/clean/"]',
                    allow_multiple=True)
                if not urls:
                    continue
                url = urls[0]
                asw_id = re.findall('(\d+)$', entry.link)[0]
                title = '%s: %s' % (entry.title, asw_id)
                text = entry.summary.title( 'img[src*="/clean/"]',
                    allow_multiple=True)[0]
                return CrawlerImage(url, title, text)
