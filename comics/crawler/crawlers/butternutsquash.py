from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.butternutsquash.net/comics/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%Y-%m-%d'),
        }
