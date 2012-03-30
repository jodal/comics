from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Hipster Hitler'
    language = 'en'
    url = 'http://www.hipsterhitler.com/'
    start_date = '2010-08-01'
    rights = 'JC & APK'

class Crawler(CrawlerBase):
    history_capable_days = 120
    schedule = None
    time_zone = 0

    def crawl(self, pub_date):
        feed = self.parse_feed('http://hipsterhitler.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            url = entry.content0.src('img')
            title = entry.title
            return CrawlerImage(url, title)
