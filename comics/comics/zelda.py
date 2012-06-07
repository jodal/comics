from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Zelda'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/zelda/'
    start_date = '2012-06-07'
    rights = 'Lina Neidestam'

class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = 1

    def crawl(self, pub_date):
        page_url = 'http://www.dagbladet.no/tegneserie/zelda/?%s' % (
            self.date_to_epoch(pub_date),)
        page = self.parse_page(page_url)
        url = page.src('img#zelda-stripe')
        return CrawlerImage(url)
