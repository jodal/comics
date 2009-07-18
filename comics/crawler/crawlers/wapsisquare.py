import re

from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Wapsi Square'
    language = 'en'
    url = 'http://www.wapsisquare.com/'
    start_date = '2001-09-09'
    history_capable_date = '2001-09-09'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Paul Taylor'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://wapsisquare.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image
                and (image['src'].startswith('/comics/')
                    or ('alt' in image and image['alt'] == "Today's Comic"))):
                m = re.match('.*/\d+_(\w+)\..*', image['src'])
                if m:
                    self.title = m.groups()[0]
                self.url = self.join_web_url(image['src'])
                return
