from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'For Better or For Worse'
    language = 'en'
    url = 'http://www.gocomics.com/forbetterorforworse'
    start_date = '1981-11-23'
    rights = 'Lynn Johnston'


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '1981-11-23'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('forbetterorforworse', pub_date)
