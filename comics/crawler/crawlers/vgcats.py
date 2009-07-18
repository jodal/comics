import datetime as dt

from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'VG Cats'
    language = 'en'
    url = 'http://www.vgcats.com/'
    start_date = '2001-09-09'
    history_capable_date = '2001-09-09'
    time_zone = -5
    rights = 'Scott Ramsoomair'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        # FIXME: Seems like they are using gif images now and then

        if self.pub_date < dt.date(2003, 5, 1):
            ext = 'gif'
        else:
            ext = 'jpg'

        self.url = 'http://www.vgcats.com/comics/images/%(date)s.%(ext)s' % {
            'date': self.pub_date.strftime('%y%m%d'),
            'ext': ext,
        }
