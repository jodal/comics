from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Charliehorse'
    language = 'en'
    url = 'http://www.krakowstudios.com/'
    start_date = '2009-01-01'
    rights = 'Iron Muse Media'

class Crawler(CrawlerBase):
    history_capable_date = '2009-01-01'
    time_zone = -5

    def crawl(self, pub_date):
        page_url = 'http://www.krakowstudios.com/archive.php?date=%s' % \
            pub_date.strftime('%Y%m%d')
        page = self.parse_page(page_url)
        image_url = page.src('img[src*="comics/"]')
        return CrawlerImage(image_url)
