from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "Fredo & Pid'jin"
    language = 'en'
    url = 'http://www.pidjin.net/'
    start_date = '2006-02-19'
    rights = 'Tudor Muscalu & Eugen Erhan'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/Pidjin')
        for entry in feed.for_date(pub_date):
            result = []
            for i in range(1, 10):
                url = entry.content0.src('img[src$="000%d.jpg"]' % i)
                text = entry.content0.title('img[src$="000%d.jpg"]' % i)
                if url and text:
                    result.append(CrawlerImage(url, text=text))
            if result:
                result[0].title = entry.title
            return result
