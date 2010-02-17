from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Baby Blues'
    language = 'en'
    url = 'http://www.arcamax.com/babyblues'
    start_date = '1990-01-01'
    rights = 'Rick Kirkman and Jerry Scott, for King Features Syndicate, Inc.'

class Crawler(CrawlerBase):
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        page = self.parse_page('http://www.arcamax.com/babyblues')
        url = page.src('img[alt^="Baby Blues Cartoon"]')
        return CrawlerImage(url)
