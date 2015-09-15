from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Unsounded'
    language = 'en'
    url = 'http://www.casualvillain.com/Unsounded/'
    start_date = '2009-10-25'
    rights = 'Ashley Cope'


class Crawler(CrawlerBase):
    history_capable_days = 50
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.casualvillain.com/Unsounded/feed/')
        for entry in feed.for_date(pub_date):
            page_url = entry.summary.href('a[href*="/comic/"]')
            page = self.parse_page(page_url)
            url = page.src('#comic img')
            title = entry.title
            return CrawlerImage(url, title)
