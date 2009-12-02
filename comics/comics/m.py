from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'M'
    language = 'no'
    url = 'http://www.madseriksen.no/'
    start_date = '2003-02-10'
    history_capable_date = '2005-01-31'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1
    rights = 'Mads Eriksen'

class Crawler(CrawlerBase):
    has_rerun_releases = True

    def crawl(self, pub_date):
        url = 'http://g2.start.no/tegneserier/striper/m/mstriper/m%(date)s.gif' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        return CrawlerResult(url)
