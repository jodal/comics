from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.bt.no/gfx/cartoons/pondus/%(date)s.gif' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
