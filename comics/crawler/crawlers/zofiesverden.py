from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.url = 'http://www.dagbladet.no/tegneserie/zofiesverdenarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(self.pub_date),
        }
