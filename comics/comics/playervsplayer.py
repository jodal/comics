from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Player vs Player'
    language = 'en'
    url = 'http://www.pvponline.com/'
    start_date = '1998-05-04'
    rights = 'Scott R. Kurtz'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/Pvponline')
        for entry in feed.for_date(pub_date):
            if not entry.title.startswith('Comic:'):
                continue
            page = self.parse_page(entry.link)
            url = page.src('.post img[src*="/comic/"]')
            title = entry.title.replace('Comic: ', '')
            if url is not None:
                return CrawlerImage(url, title)
