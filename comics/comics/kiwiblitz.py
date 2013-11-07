from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Kiwiblitz'
    language = 'en'
    url = 'http://www.kiwiblitz.com/'
    start_date = '2009-04-18'
    rights = 'Mary Cagle'


class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'We,Fr'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.kiwiblitz.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if not url:
                continue
            url = url.replace('-150x150', '')
            title = entry.title
            return CrawlerImage(url, title)
