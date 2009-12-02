from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = '8-Bit Theater'
    language = 'en'
    url = 'http://www.nuklearpower.com/'
    start_date = '2001-03-02'
    history_capable_date = '2001-03-02'
    schedule = 'Tu,Th,Sa'
    time_zone = -6
    rights = 'Brian Clevinger'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page_url = 'http://www.nuklearpower.com/%(year)s/%(month)d/%(day)s/episode/' % {
            'year': pub_date.year,
            'month': pub_date.month,
            'day': pub_date.day
        }
        page = self.parse_page(page_url)
        url = page.src('img[src^="http://www.nuklearpower.com/comics/"]')
        title = page.alt('img[src^="http://www.nuklearpower.com/comics/"]')
        return CrawlerResult(url, title)
