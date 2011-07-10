from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Nemi (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/bergenpuls/tegneserier/tegneserier_nemi/'
    start_date = '1997-01-01'
    rights = 'Lise Myhre'

class Crawler(CrawlerBase):
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.bt.no/external/cartoon/nemi/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
