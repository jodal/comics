from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Deathbulge'
    language = 'en'
    url = 'http://www.deathbulge.com/'
    start_date = '2012-06-13'
    rights = 'Deathbulge'


class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.deathbulge.com/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            return CrawlerImage(url)
