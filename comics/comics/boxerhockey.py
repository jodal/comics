from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Boxer Hockey'
    language = 'en'
    url = 'http://boxerhockey.fireball20xl.com/'
    start_date = '2007-11-25'
    rights = 'Tyson "Rittz" Hesse'

class Crawler(CrawlerBase):
    time_zone = -7
    history_capable_days = 30

    def crawl(self, pub_date):
        feed = self.parse_feed('http://boxerhockey.fireball20xl.com/inc/feed.php')
        for entry in feed.for_date(pub_date):
            title = entry.title
            page_uri = entry.link
            page = self.parse_page(page_uri)
            url = page.src('img#comicimg')
            text = None

            return CrawlerImage(url, title, text)
