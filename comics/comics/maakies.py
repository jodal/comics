from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'MAAKIES'
    language = 'en'
    url = 'http://www.maakies.com/'
    start_date = '2012-01-01'
    rights = 'Jacob Convey'


class Crawler(CrawlerBase):
    time_zone = 'US/Eastern'
    history_capable_days = 200
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.maakies.com/?feed=rss2')
        for entry in feed.for_date(pub_date):
            url = entry.content0.href('a[href^="http://www.maakies.com/wp-content/uploads"]')
            return CrawlerImage(url)
