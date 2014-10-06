from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Nemi (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/nemi/'
    start_date = '1997-01-01'
    rights = 'Lise Myhre'


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        url = 'http://www.dagbladet.no/tegneserie/nemiarkiv/serve.php?%s' % (
            epoch,)
        return CrawlerImage(url)
