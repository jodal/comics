from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'User Friendly'
    language = 'en'
    url = 'http://www.userfriendly.org/'
    start_date = '1997-11-17'
    history_capable_date = '1997-11-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'J.D. "Illiad" Frazer'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        page_url = 'http://ars.userfriendly.org/cartoons/?id=%(date)s' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        page = self.parse_page(page_url)
        self.url = page.src('img[alt^="Strip for"]')
