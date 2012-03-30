from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Liberty Meadows'
    language = 'en'
    url = 'http://www.creators.com/comics/liberty-meadows.html'
    start_date = '1997-03-30'
    end_date = '2001-12-31'
    rights = 'Frank Cho'

class Crawler(CrawlerBase):
    history_capable_days = 19
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.creators.com/comics/liberty-meadows.rss')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="_thumb"]').replace('thumb', 'image')
            return CrawlerImage(url)
