from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Zofies verden'
    language = 'no'
    url = 'http://www.zofiesverden.no/'
    start_date = '2006-05-02'
    rights = 'Grethe Nestor & Norunn Blichfeldt Schjerven'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date, 'Europe/Oslo')
        url = ('http://www.dagbladet.no/tegneserie/' +
            'zofiesverdenarkiv/serve.php?%d' % epoch)
        return CrawlerImage(url)
