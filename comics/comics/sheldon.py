from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Sheldon'
    language = 'en'
    url = 'http://www.sheldoncomics.com/'
    start_date = '2001-11-30'
    rights = 'Dave Kellett'


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://cdn.sheldoncomics.com/rss.xml')
        for entry in feed.for_date(pub_date):
            if 'Comic' not in entry.tags:
                continue
            url = entry.content0.src('img[src*="/strips/"]')
            return CrawlerImage(url)
