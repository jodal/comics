from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'F@NB0Y$'
    language = 'en'
    url = 'http://fanboys-online.com/'
    start_date = '2006-04-19'
    rights = 'Scott Dewitt'

class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://fanboys-online.com/rss/comic.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Comic:'):
                title = entry.title.replace('Comic: ', '')
                url = 'http://fanboys-online.com/comics/%s.jpg' % (
                    pub_date.strftime('%Y%m%d'),)
                return CrawlerImage(url, title)
