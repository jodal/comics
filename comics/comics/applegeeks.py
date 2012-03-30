from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'AppleGeeks'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2003-01-01'
    rights = 'Mohammad Haque & Ananth Panagariya'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = None
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.applegeeks.com/rss/?cat=comic')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img').replace('thumb.gif', '.jpg')
            title = entry.title
            return CrawlerImage(url, title)
