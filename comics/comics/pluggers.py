from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Pluggers'
    language = 'en'
    url = 'http://www.gocomics.com/pluggers'
    start_date = '2001-04-08'
    rights = 'Gary Brookins'

class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '2001-04-08'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('Pluggers', pub_date)
