from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Ctrl+Alt+Del Sillies'
    language = 'en'
    url = 'http://www.cad-comic.com/sillies/'
    start_date = '2008-06-27'
    rights = 'Tim Buckley'

class Crawler(CrawlerBase):
    history_capable_date = '2008-06-27'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://www.cad-comic.com/comics/sillies/%s.gif' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerResult(url)
