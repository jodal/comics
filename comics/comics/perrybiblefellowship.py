from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'The Perry Bible Fellowship'
    language = 'en'
    url = 'http://www.pbfcomics.com/'
    start_date = '2001-01-01'
    rights = 'Nicholas Gurewitch'


class Crawler(CrawlerBase):
    history_capable_date = '2001-01-01'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.pbfcomics.com/feed/feed.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/archive_b/"]')
            title = entry.title
            return CrawlerImage(url, title)
