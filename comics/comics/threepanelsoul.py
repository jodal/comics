from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Three Panel Soul'
    language = 'en'
    url = 'http://www.threepanelsoul.com/'
    start_date = '2006-11-05'
    rights = 'Ian McConville & Matt Boyd'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://threepanelsoul.com/feed/')
        for entry in feed.for_date(pub_date):
            title = entry.title
            url = entry.content0.src('img[src*="/comics-rss/"]')
            if url is not None:
                url = url.replace('-rss', '')
                return CrawlerImage(url, title)
