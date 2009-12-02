from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Penny Arcade'
    language = 'en'
    url = 'http://www.penny-arcade.com/'
    start_date = '1998-11-18'
    history_capable_date = '1998-11-18'
    schedule = 'Mo,We,Fr'
    rights = 'Mike Krahulik & Jerry Holkins'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page_url = 'http://www.penny-arcade.com/comic/%(date)s/' % {
            'date': pub_date.strftime('%Y/%m/%d'),
        }
        page = self.parse_page(page_url)
        # FIXME The decode() part should be handled by CrawlerBase
        title = page.text('h1').decode('iso-8859-1')
        url = page.src('img[alt="%s"]' % title)
        return CrawlerResult(url, title)
