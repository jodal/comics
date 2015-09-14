from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Non Sequitur'
    language = 'en'
    url = 'http://www.gocomics.com/nonsequitur'
    start_date = '1992-02-16'
    rights = 'Wiley Miller'


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '1992-02-16'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('nonsequitur', pub_date)
