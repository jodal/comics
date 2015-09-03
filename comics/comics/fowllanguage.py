from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Fowl Language'
    language = 'en'
    url = 'http://www.fowllanguagecomics.com/'
    start_date = '2013-07-22'
    rights = 'Brian Gordon'


class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.fowllanguagecomics.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img.wp-post-image')
            if url is None:
                continue
            url = url.replace('?resize=150%2C150', '')
            title = entry.title
            return CrawlerImage(url, title)
