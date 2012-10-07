from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Chopping Block'
    language = 'en'
    url = 'http://choppingblock.keenspot.com/'
    start_date = '2000-07-25'
    rights = 'Lee Adam Herold'

class Crawler(CrawlerBase):
    history_capable_date = '2000-07-25'
    schedule = 'We'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        url = 'http://choppingblock.keenspot.com/comics/cb%s.jpg' % (
            pub_date.strftime('%Y%m%d'))
        return CrawlerImage(url)
