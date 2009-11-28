from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Something Positive'
    language = 'en'
    url = 'http://www.somethingpositive.net/'
    start_date = '2001-12-19'
    history_capable_date = '2001-12-19'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'R. K. Milholland'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.somethingpositive.net/arch/sp%(date)s.gif' % {
            'date': self.pub_date.strftime('%m%d%Y'),
        }
