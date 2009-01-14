from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://pub.tv2.no/nettavisen/tegneserie/pondus/veslemoy/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%d%m%y'),
        }
