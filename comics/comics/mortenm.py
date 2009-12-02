from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Morten M (vg.no)'
    language = 'no'
    url = 'http://www.vg.no/spesial/mortenm/'
    start_date = '1978-01-01'
    rights = 'Morten M. Kristiansen'

class Crawler(CrawlerBase):
    history_capable_days = 120
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://static.vg.no/gfx/mortenm/output/%s.jpg' % (
            pub_date.strftime('%Y/%m/%Y-%m-%d'),)
        return CrawlerResult(url)
