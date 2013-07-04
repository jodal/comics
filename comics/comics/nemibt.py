from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Nemi (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/bergenpuls/tegneserier/tegneserier_nemi/'
    start_date = '1997-01-01'
    rights = 'Lise Myhre'


class Crawler(CrawlerBase):
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://www.bt.no/external/cartoon/nemi/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
