from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.rocky import ComicData as RockyData


class ComicData(RockyData):
    name = 'Rocky (bt.no)'
    url = 'http://www.bt.no/bergenpuls/tegneserier/tegneserier_rocky/'


class Crawler(CrawlerBase):
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://www.bt.no/external/cartoon/rocky/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
