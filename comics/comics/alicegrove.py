from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Alice Grove'
    language = 'en'
    url = 'http://alicegrove.com'
    start_date = '2014-01-01'
    rights = 'Jeph Jacques'


class Crawler(CrawlerBase):
    history_capable_days = 20
   #schedule = 'Tu,Th,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.alicegrove.com/rss')
        for entry in feed.for_date(pub_date):
            url = entry.description.src('img[src*="media.tumblr.com"]')
            title = entry.title
            return CrawlerImage(url, title)
