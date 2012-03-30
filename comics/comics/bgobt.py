from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Business Guys on Business Trips'
    language = 'en'
    url = 'http://www.businessguysonbusinesstrips.com/'
    start_date = '2007-07-12'
    rights = '"Managing Director"'

class Crawler(CrawlerBase):
    history_capable_days = 100
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://businessguysonbusinesstrips.com/?feed=atom')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            page.remove('img[src$="/art/wgp_banner.jpg"]')
            url = page.src(
                'img[src^="http://businessguysonbusinesstrips.com/art/"]')
            title = entry.title
            return CrawlerImage(url, title)
