from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Zofies verden'
    language = 'no'
    url = 'http://www.zofiesverden.no/'
    start_date = '2006-05-02'
    end_date='2012-08-31'
    active=False
    rights = 'Grethe Nestor & Norunn Blichfeldt Schjerven'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        url = ('http://www.dagbladet.no/tegneserie/' +
            'zofiesverdenarkiv/serve.php?%d' % epoch)
        return CrawlerImage(url)
