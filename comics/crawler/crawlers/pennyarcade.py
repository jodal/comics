from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'Penny Arcade'
    language = 'en'
    url = 'http://www.penny-arcade.com/'
    start_date = '1998-11-18'
    history_capable_date = '1998-11-18'
    schedule = 'Mo,We,Fr'
    rights = 'Mike Krahulik & Jerry Holkins'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.penny-arcade.com/comic/%(date)s/' % {
            'date': self.pub_date.strftime('%Y/%m/%d'),
        }

        page = LxmlParser(self.web_url)

        self.title = page.text('div.simpleheader')
        self.url = page.src('img[alt="%s"]' % self.title)
