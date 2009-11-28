from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'M'
    language = 'no'
    url = 'http://www.madseriksen.no/'
    start_date = '2003-02-10'
    history_capable_date = '2005-01-31'
    has_reruns = True
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1
    rights = 'Mads Eriksen'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://g2.start.no/tegneserier/striper/m/mstriper/m%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
