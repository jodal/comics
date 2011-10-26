from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Extra Ordinary'
    language = 'en'
    url = 'http://www.extracomics.com/'
    start_date = '2009-12-14'
    rights = 'Li Chen'

class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'We'
    time_zone = -7

    # Without Referer set, the server returns 403 Forbidden
    headers = {'Referer': 'http://www.exocomics.com/'}

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.exocomics.com/feed')
        for entry in feed.for_date(pub_date):
            title = entry.title
            page = self.parse_page(entry.link)
            url = page.src('img.comic-item')
            text = page.title('img.comic-item')
            return CrawlerImage(url, title, text)
