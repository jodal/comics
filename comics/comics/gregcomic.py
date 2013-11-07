from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Greg Comic'
    language = 'en'
    url = 'http://gregcomic.com/'
    start_date = '2011-06-01'
    rights = 'Chur Yin Wan'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://gregcomic.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            title = entry.title
            url = entry.summary.src('img[src*="/comics-rss/"]')
            if not url:
                continue
            url = url.replace('-rss', '')
            return CrawlerImage(url, title)
