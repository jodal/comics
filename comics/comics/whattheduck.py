from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'What the Duck'
    language = 'en'
    url = 'http://www.whattheduck.net/'
    start_date = '2006-07-01'
    rights = 'Aaron Johnson'


class Crawler(CrawlerBase):
    history_capable_days = 28
    time_zone = 'US/Central'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.whattheduck.net/rss')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src$=".gif"]')
            return CrawlerImage(url)
