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
        url = ('http://www.dagbladet.no/tegneserie/' +
            'zofiesverdenarkiv/serve.php?%d' % self.date_to_epoch(pub_date))
        return CrawlerImage(url)
