from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.brinkcomic.com/comics/%(date)s.gif' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }

    def _get_headers(self):
        return {
            'Referer': 'http://www.brinkcomic.com/d/%(date)s/' % {
                'date': self.pub_date.strftime('%Y%m%d'),
            }
        }
