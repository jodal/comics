from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'you and me and cats'
    language = 'en'
    url = 'http://strawberry-pie.net/yamac/'
    start_date = '2009-07-01'
    rights = 'bubble'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://strawberry-pie.net/yamac/?feed=rss2')
        for entry in feed.for_date(pub_date):
            if 'comic' not in entry.tags:
                continue
            url = entry.summary.src('img')
            url = url.replace('comics-rss', 'comics')
            title = entry.title
            return CrawlerImage(url, title)
