from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Zelda'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/zelda/'
    start_date = '2012-06-07'
    rights = 'Lina Neidestam'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date, 'Europe/Oslo')
        page_url = 'http://www.dagbladet.no/tegneserie/zelda/?%s' % epoch
        page = self.parse_page(page_url)
        url = page.src('img#zelda-stripe')
        return CrawlerImage(url)
