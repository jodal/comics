from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Reveland'
    language = 'no'
    url = 'http://reveland.nettserier.no/'
    start_date = '2007-03-20'
    rights = 'Jorunn Hanto-Haugse'

class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'Mo,We,Fr'
    time_zone = 1

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date, 'Europe/Oslo')
        url = 'http://reveland.nettserier.no/_striper/reveland-%s.jpg' % epoch
        return CrawlerImage(url)
