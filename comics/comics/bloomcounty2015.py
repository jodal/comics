from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Bloom County 2015'
    language = 'en'
    url = 'http://www.gocomics.com/bloom-county/'
    start_date = '2015-07-20'
    rights = 'Berkeley Breathed'


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '2015-07-20'
    schedule = 'Mo,Tu,We,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper(
            'Bloom County 2015', pub_date, url_name='bloom-county')
