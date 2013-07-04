from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'The Adventures of Dr. McNinja'
    language = 'en'
    url = 'http://drmcninja.com/'
    start_date = '2004-08-03'
    rights = 'Christopher Hastings'


class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://drmcninja.com/feed')
        for entry in feed.for_date(pub_date):
            if not '/comic/' in entry.link:
                continue
            url = entry.summary.src('img[src*="/comics-rss/"]')
            url = url.replace('comics-rss', 'comics')
            title = entry.title
            text = entry.summary.title('img[src*="/comics-rss/"]')
            return CrawlerImage(url, title, text)
