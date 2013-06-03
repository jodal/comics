# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Uten Sokker'
    language = 'no'
    url = 'http://utensokker.nettserier.no/'
    start_date = '2009-07-14'
    rights = 'Bjørnar Grandalen'

class Crawler(CrawlerBase):
    history_capable_date='2009-07-14'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://utensokker.nettserier.no/_striper/utensokker-%s.jpg' % (
            self.date_to_epoch(pub_date),)
        page_url = 'http://utensokker.nettserier.no/%s' % (
            pub_date.strftime('%Y/%m/%d'))
        page = self.parse_page(page_url)
        title = page.alt('img[src*="/_striper/"]')
        return CrawlerImage(url, title)
