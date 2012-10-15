from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Rocky (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rocky/'
    start_date = '1998-01-01'
    rights = 'Martin Kellerman'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        url = 'http://www.dagbladet.no/tegneserie/rockyarkiv/serve.php?%s' % (
            epoch,)
        return CrawlerImage(url)
