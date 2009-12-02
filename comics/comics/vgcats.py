import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'VG Cats'
    language = 'en'
    url = 'http://www.vgcats.com/'
    start_date = '2001-09-09'
    history_capable_date = '2001-09-09'
    time_zone = -5
    rights = 'Scott Ramsoomair'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        # FIXME: Seems like they are using gif images now and then
        if pub_date < dt.date(2003, 5, 1):
            ext = 'gif'
        else:
            ext = 'jpg'
        url = 'http://www.vgcats.com/comics/images/%(date)s.%(ext)s' % {
            'date': pub_date.strftime('%y%m%d'),
            'ext': ext,
        }
        return CrawlerResult(url)
