from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Apokalips Web Comic'
    language = 'en'
    url = 'http://www.myapokalips.com/'
    start_date = '2009-02-13'
    end_date = '2011-07-04'
    active = False
    rights = 'Mike Gioia, CC BY-NC 2.5'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
