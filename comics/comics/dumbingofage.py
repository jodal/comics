from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dumbing of Age'
    language = 'en'
    url = 'http://www.dumbingofage.com/'
    start_date = '2010-09-10'
    rights = 'David Willis'


class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.dumbingofage.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics-rss/"]')
            if url is None:
                continue
            url = url.replace('/comics-rss/', '/comics/')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics-rss/"]')
            return CrawlerImage(url, title, text)
