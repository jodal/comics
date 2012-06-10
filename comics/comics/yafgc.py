from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Yet Another Fantasy Gamer Comic'
    language = 'en'
    url = 'http://www.yafgc.net/'
    start_date = '2006-05-29'
    rights = 'Rich Morris'

class Crawler(CrawlerBase):
    history_capable_date = '2006-05-29'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://yafgc.net/inc/feed.php')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/img/comic/"]')
            title = entry.title
            return CrawlerImage(url, title)
