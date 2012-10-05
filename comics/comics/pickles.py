from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Pickles'
    language = 'en'
    url = 'http://www.arcamax.com/thefunnies/pickles'
    start_date = '2003-10-01'
    rights = 'Brian Crane'

class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '2003-10-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('Pickles', pub_date)
