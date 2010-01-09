from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'ExtraLife'
    language = 'en'
    url = 'http://www.myextralife.com/'
    start_date = '2001-06-17'
    rights = 'Scott Johnson'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.myextralife.com/feed/')
        for entry in feed.for_date(pub_date):
            if not '/comic/' in entry.link:
                continue
            url = entry.summary.src('img[src*="/comics-rss/"]')
            url = url.replace('/comics-rss/', '/comics/')
            title = entry.summary.title('img[src*="/comics-rss/"]')
            title = title.replace('Comic: ', '')
            title = title.replace(u'\u201c', '')
            title = title.replace(u'\u201d', '')
            return CrawlerResult(url, title)
