from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.myextralife.com/strips/%(date)s.jpg' % {
            'date': self.pub_date.strftime('%m-%d-%Y'),
        }
