from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'ExtraLife'
    language = 'en'
    url = 'http://www.myextralife.com/'
    start_date = '2001-06-17'
    history_capable_date = '2001-06-17'
    schedule = 'Mo,We,Fr'
    time_zone = -7
    rights = 'Scott Johnson'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.myextralife.com/strips/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%m-%d-%Y'),
        }
