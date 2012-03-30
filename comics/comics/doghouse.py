from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'The Doghouse Diaries'
    language = 'en'
    url = 'http://www.thedoghousediaries.com/'
    start_date = '2009-01-08'
    rights = 'Will, Ray, & Raf'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/thedoghousediaries/feed')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/comics/"]')
            title = entry.content0.alt('img[src*="/comics/"]')
            text = entry.content0.title('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
