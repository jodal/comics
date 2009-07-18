from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'F@NB0Y$'
    language = 'en'
    url = 'http://fanboys-online.com/'
    start_date = '2006-04-19'
    history_capable_days = 50
    time_zone = -5
    rights = 'Scott Dewitt'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://fanboys-online.com/rss/comic.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Comic:')):
                self.title = entry.title.replace('Comic: ', '')
                self.url = 'http://fanboys-online.com/comics/%(date)s.jpg' % {
                    'date': self.pub_date.strftime('%Y%m%d'),
                }
                return
