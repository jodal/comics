from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Devil Bear'
    language = 'en'
    url = 'http://www.thedevilbear.com/'
    start_date = '2009-01-01'
    history_capable_days = 0
    schedule = 'Mo'
    time_zone = -8
    rights = 'Ben Bourbon'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page = self.parse_page('http://www.thedevilbear.com/')
        url = page.src('#cg_img img')
        return CrawlerResult(url)
