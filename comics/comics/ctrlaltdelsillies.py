from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Ctrl+Alt+Del Sillies'
    language = 'en'
    url = 'http://www.cad-comic.com/sillies/'
    start_date = '2008-06-27'
    rights = 'Tim Buckley'

class Crawler(CrawlerBase):
    history_capable_date = '2008-06-27'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://www.cad-comic.com/comics/sillies/%s.gif' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerImage(url)
