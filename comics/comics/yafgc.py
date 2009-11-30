from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Yet Another Fantasy Gamer Comic'
    language = 'en'
    url = 'http://yafgc.shipsinker.com/'
    start_date = '2006-05-29'
    history_capable_date = '2006-05-29'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Rich Morris'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.url = 'http://yafgc.shipsinker.com/istrip_files/strips/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
