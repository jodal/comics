from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'The Idle State'
    language = 'en'
    url = 'http://www.theidlestate.com/'
    start_date = '2011-07-18'
    rights = 'Nick Wright'

class Crawler(CrawlerBase):
    history_capable_days = None
    schedule = 'Mo,We,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        page = self.parse_page('http://www.theidlestate.com')
        url = page.src('img[src*="/wp-content/webcomic/idlestate/"]')
        return CrawlerImage(url)
