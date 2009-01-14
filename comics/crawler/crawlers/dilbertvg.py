from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.vg.no/grafikk/dilbert/dilbert-%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y-%m-%d'),
        }
