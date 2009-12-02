from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Business Guys on Business Trips'
    language = 'en'
    url = 'http://www.businessguysonbusinesstrips.com/'
    start_date = '2007-07-12'
    history_capable_days = 100
    schedule = 'Mo'
    time_zone = -7

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://businessguysonbusinesstrips.com/?feed=atom')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            page.remove('img[src$="/art/wgp_banner.jpg"]')
            url = page.src(
                'img[src^="http://businessguysonbusinesstrips.com/art/"]')
            title = entry.title
            return CrawlerResult(url, title)
