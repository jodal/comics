from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Bunny'
    language = 'en'
    url = 'http://bunny-comic.com/'
    start_date = '2004-08-22'
    rights = 'H. Davies, CC BY-NC-SA'

class Crawler(CrawlerBase):
    history_capable_days = 0
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.bunny-comic.com/rss/bunny.xml')
        for entry in feed.all():
            url = entry.summary.src('img[src*="/strips/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/strips/"]')
            return CrawlerImage(url, title, text)
