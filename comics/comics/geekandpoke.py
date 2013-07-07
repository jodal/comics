from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Geek and Poke'
    language = 'en'
    url = 'http://geek-and-poke.com/'
    start_date = '2006-08-22'
    rights = 'Oliver Widder, CC BY-ND 2.0'


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'Europe/Berlin'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/GeekAndPoke')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/static/"]')
            title = entry.title
            return CrawlerImage(url, title)
