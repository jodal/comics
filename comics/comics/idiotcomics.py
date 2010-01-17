from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Idiot Comics'
    language = 'en'
    url = 'http://www.idiotcomics.com/'
    start_date = '2006-09-08'
    rights = 'Robert Sergel'

class Crawler(CrawlerBase):
    history_capable_days = 500
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Tu'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/idiotcomics.xml')
        for entry in feed.for_date(pub_date):
            result = []
            for img in entry.summary.root.cssselect('img'):
                url = img.get('src')
                result.append(CrawlerImage(url))
            if result:
                result[0].title = entry.title
            return result
