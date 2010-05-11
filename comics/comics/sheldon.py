from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Sheldon'
    language = 'en'
    url = 'http://www.sheldoncomics.com/'
    start_date = '2001-11-30'
    rights = 'Dave Kellett'

class Crawler(CrawlerBase):
    history_capable_date = Meta.start_date
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        filetype = 'gif'
        if pub_date.weekday() in [5,6]: filetype = 'jpg'
        url = 'http://www.sheldoncomics.com/strips/%s.%s' % (
                pub_date.strftime('sd%y%m%d'), filetype)
        title = 'strip for %s' % pub_date.strftime('%B / %d / %Y')
        return CrawlerImage(url, title)
