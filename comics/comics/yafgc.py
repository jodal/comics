from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Yet Another Fantasy Gamer Comic'
    language = 'en'
    url = 'http://www.yafgc.net/'
    start_date = '2006-05-29'
    rights = 'Rich Morris'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://yafgc.net/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if not url:
                continue
            url = url.replace('-150x150', '')
            title = entry.title
            return CrawlerImage(url, title)
