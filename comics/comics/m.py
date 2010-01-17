from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'M'
    language = 'no'
    url = 'http://www.madseriksen.no/'
    start_date = '2003-02-10'
    rights = 'Mads Eriksen'

class Crawler(CrawlerBase):
    history_capable_date = '2005-01-31'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1
    has_rerun_releases = True

    def crawl(self, pub_date):
        url = 'http://g2.start.no/tegneserier/striper/m/mstriper/m%s.gif' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerImage(url)
