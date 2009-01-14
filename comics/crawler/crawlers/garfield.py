from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://images.ucomics.com/comics/ga/%(year)s/ga%(date)s.gif' % {
            'year': self.pub_date.strftime('%Y'),
            'date': self.pub_date.strftime('%y%m%d'),
        }
