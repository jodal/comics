from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Boxer Hockey'
    language = 'en'
    url = 'http://boxerhockey.fireball20xl.com/'
    start_date = '2007-11-25'
    rights = 'Tyson "Rittz" Hesse'

class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://boxerhockey.fireball20xl.com/inc/feed.php')
        for entry in feed.for_date(pub_date):
            title = entry.title
            page = self.parse_page(entry.link)
            url = page.src('img#comicimg')
            return CrawlerImage(url, title)
