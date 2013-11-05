from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pole Dancing Adventures'
    language = 'en'
    url = 'http://pole-dancing-adventures.blogspot.com/'
    start_date = '2010-01-28'
    rights = 'Leen Isabel'


class Crawler(CrawlerBase):
    history_capable_date = '2010-01-28'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feed.feedburner.com/blogspot/zumUM')
        for entry in feed.for_date(pub_date):
            url = entry.sunnary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
