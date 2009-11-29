from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'F@NB0Y$'
    language = 'en'
    url = 'http://fanboys-online.com/'
    start_date = '2006-04-19'
    history_capable_days = 180
    time_zone = -5
    rights = 'Scott Dewitt'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://fanboys-online.com/rss/comic.xml')
        for entry in feed.for_date(self.pub_date):
            if entry.title.startswith('Comic:'):
                self.title = entry.title.replace('Comic: ', '')
                self.url = 'http://fanboys-online.com/comics/%(date)s.jpg' % {
                    'date': self.pub_date.strftime('%Y%m%d'),
                }
