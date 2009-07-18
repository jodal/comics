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
        self.web_url = 'http://ars.userfriendly.org/cartoons/?id=%(date)s' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        self.parse_web_page()

        for img in self.web_page.imgs:
            if ('src' in img and 'alt' in img
                and img['alt'].startswith('Strip for')):
                self.url = self.join_web_url(img['src'])
                return
