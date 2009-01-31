from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.cad-comic.com/comics/Lite%(date)s.jpg' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
