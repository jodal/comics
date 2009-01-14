from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dieselsweeties.com/print/strips/ds%(date)s.png' \
        % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
