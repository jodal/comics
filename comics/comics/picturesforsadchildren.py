from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'pictures for sad children'
    language = 'en'
    url = 'http://picturesforsadchildren.com/'
    start_date = '2007-01-01'
    rights = 'John Campbell'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://picturesforsadchildren.com/rss')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            return CrawlerImage(url)
