from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = '8-Bit Theater'
    language = 'en'
    url = 'http://www.nuklearpower.com/'
    start_date = '2001-03-02'
    rights = 'Brian Clevinger'

class Crawler(CrawlerBase):
    history_capable_date = '2001-03-02'
    schedule = 'Tu,Th,Sa'
    time_zone = -6

    def crawl(self, pub_date):
        page_url = 'http://www.nuklearpower.com/%s/episode/' % (
            pub_date.strftime('%Y/%m/%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[src^="http://www.nuklearpower.com/comics/"]')
        title = page.alt('img[src^="http://www.nuklearpower.com/comics/"]')
        return CrawlerResult(url, title)
