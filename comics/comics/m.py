from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'M'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/m'
    start_date = '2003-02-10'
    rights = 'Mads Eriksen'

class Crawler(CrawlerBase):
    history_capable_date = '2011-03-02'
    schedule = 'Mo,We,Fr'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/markiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
