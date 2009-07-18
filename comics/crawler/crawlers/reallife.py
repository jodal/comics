from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Real Life'
    language = 'en'
    url = 'http://www.reallifecomics.com/'
    start_date = '1999-11-15'
    history_capable_date = '1999-11-15'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Greg Dean'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.reallifecomics.com/archive/%(date)s.html' % {
            'date': self.pub_date.strftime('%y%m%d'),
        }
        self.parse_web_page()

        for img in self.web_page.imgs:
            if ('src' in img and 'alt' in img
                and img['alt'].startswith('strip for')):
                self.url = self.join_web_url(img['src'])
                return
