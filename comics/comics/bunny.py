from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Bunny'
    language = 'en'
    url = 'http://bunny-comic.com/'
    start_date = '2004-08-22'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'H. Davies, CC BY-NC-SA'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.bunny-comic.com/rss/bunny.xml')
        for entry in feed.all():
            image_name = entry.summary.src('img[src*="/strips/"]').replace(
                'http://bunny-comic.com/strips/', '')
            if (image_name[:6].isdigit()
                    and pub_date == self.string_to_date(
                    image_name[:6], '%d%m%y')):
                url = entry.summary.src('img[src*="/strips/"]')
                title = entry.title
                text = entry.summary.alt('img[src*="/strips/"]')
                return CrawlerResult(url, title, text)
