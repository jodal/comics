from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'F@NB0Y$'
    language = 'en'
    url = 'http://fanboys-online.com/'
    start_date = '2006-04-19'
    history_capable_days = 180
    time_zone = -5
    rights = 'Scott Dewitt'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://fanboys-online.com/rss/comic.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Comic:'):
                title = entry.title.replace('Comic: ', '')
                url = 'http://fanboys-online.com/comics/%(date)s.jpg' % {
                    'date': pub_date.strftime('%Y%m%d'),
                }
                return CrawlerResult(url, title)
