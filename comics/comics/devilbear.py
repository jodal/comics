from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Devil Bear'
    language = 'en'
    url = 'http://www.thedevilbear.com/'
    start_date = '2009-01-01'
    rights = 'Ben Bourbon'

class Crawler(CrawlerBase):
    history_capable_days = 0
    time_zone = -8

    def crawl(self, pub_date):
        page = self.parse_page('http://www.thedevilbear.com/')
        url = page.src('#cg_img img')
        return CrawlerImage(url)
