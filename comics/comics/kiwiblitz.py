from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Kiwi Blitz'
    language = 'en'
    url = 'http://www.kiwiblitz.com/'
    start_date = '2009-04-18'
    rights = 'Mary Cagle'


class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = 'Th'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.kiwiblitz.com/rss.php')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img#cc-comic')
            title = entry.title.strip().replace('Kiwi Blitz - ', '')
            return CrawlerImage(url, title)
