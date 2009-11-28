from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Penny Arcade'
    language = 'en'
    url = 'http://www.penny-arcade.com/'
    start_date = '1998-11-18'
    history_capable_date = '1998-11-18'
    schedule = 'Mo,We,Fr'
    rights = 'Mike Krahulik & Jerry Holkins'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        page_url = 'http://www.penny-arcade.com/comic/%(date)s/' % {
            'date': self.pub_date.strftime('%Y/%m/%d'),
        }
        page = self.parse_page(page_url)

        # FIXME The decode() part should be handled by BaseComicCrawler
        self.title = page.text('h1').decode('iso-8859-1')
        self.url = page.src('img[alt="%s"]' % self.title)
