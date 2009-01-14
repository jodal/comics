import datetime as dt

from comics.crawler.crawlers import BaseComicCrawler

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
