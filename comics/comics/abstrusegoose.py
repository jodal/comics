from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Abstruse Goose'
    language = 'en'
    url = 'http://www.abstrusegoose.com/'
    start_date = '2008-02-01'
    rights = 'lcfr, CC BY-NC 3.0 US'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Th'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://abstrusegoose.com/atomfeed.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/strips/"]')
            title = entry.title
            text = entry.summary.title('img[src*="/strips/"]')
            return CrawlerImage(url, title, text)
