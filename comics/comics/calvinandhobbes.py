from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Calvin and Hobbes'
    language = 'en'
    url = 'http://www.gocomics.com/calvinandhobbes'
    start_date = '1985-11-18'
    end_date = '1995-12-31'
    rights = 'Bill Watterson'

class Crawler(GoComicsComCrawlerBase):
    history_capable_days = 31
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Mountain'

    def crawl(self, pub_date):
        return self.crawl_helper('Calvin and Hobbes', pub_date)
