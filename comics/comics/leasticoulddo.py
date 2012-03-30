from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Least I Could Do'
    language = 'en'
    url = 'http://www.leasticoulddo.com/'
    start_date = '2003-02-10'
    rights = 'Ryan Sohmer & Lar deSouza'

class Crawler(CrawlerBase):
    history_capable_date = '2003-02-10'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://www.leasticoulddo.com/comics/%s.gif' % (
            pub_date.strftime('%Y%m%d'),)
        return CrawlerImage(url)
