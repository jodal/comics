from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Cardboard Crack'
    language = 'en'
    url = 'http://cardboard-crack.com/'
    start_date = '2013-03-01'
    rights = 'Magic Addict'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://cardboard-crack.com/rss')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src$="500.gif"]')
            return CrawlerImage(url)
