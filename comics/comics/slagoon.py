from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = "Sherman's Lagoon"
    language = 'en'
    url = 'http://www.slagoon.com/'
    start_date = '1991-05-13'
    rights = 'Jim Toomey'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        url = 'http://www.slagoon.com/dailies/SL%s.gif' % (
            pub_date.strftime('%y%m%d'),)
        return CrawlerImage(url)
