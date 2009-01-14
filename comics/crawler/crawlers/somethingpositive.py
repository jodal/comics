from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.somethingpositive.net/arch/sp%(date)s.gif' % {
            'date': self.pub_date.strftime('%m%d%Y'),
        }
