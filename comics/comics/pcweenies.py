from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'The PC Weenies'
    language = 'en'
    url = 'http://pcweenies.com/'
    start_date = '1998-10-21'
    rights = 'Krishna M. Sadasivam'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,We,Fr'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://pcweenies.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src(u'img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
