from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Zofies verden'
    language = 'no'
    url = 'http://www.zofiesverden.no/'
    start_date = '2006-05-02'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Grethe Nestor & Norunn Blichfeldt Schjerven'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dagbladet.no/tegneserie/zofiesverdenarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(self.pub_date),
        }
