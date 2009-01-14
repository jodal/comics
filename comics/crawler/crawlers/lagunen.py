from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://g2.start.no/tegneserier/striper/lagunen/lag-striper/lag%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
