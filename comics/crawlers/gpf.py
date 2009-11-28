from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'General Protection Fault'
    language = 'en'
    url = 'http://www.gpf-comics.com/'
    start_date = '1998-11-02'
    history_capable_date = '1998-11-02'
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Jeffrey T. Darlington'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        page_url = 'http://www.gpf-comics.com/archive.php?d=%(date)s' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        page = self.parse_page(page_url)
        self.url = page.src('img[alt^="[Comic for"]')
