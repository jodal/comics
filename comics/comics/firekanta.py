# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Firekanta'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/firekanta'
    rights = 'Nils Axle Kanten'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        page_url = 'http://www.dagbladet.no/tegneserie/firekanta/?%s' % epoch
        page = self.parse_page(page_url)
        url = page.src('img#firekanta-stripe')
        return CrawlerImage(url)
