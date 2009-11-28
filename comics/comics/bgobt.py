from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Business Guys on Business Trips'
    language = 'en'
    url = 'http://www.businessguysonbusinesstrips.com/'
    start_date = '2007-07-12'
    history_capable_days = 100
    schedule = 'Mo'
    time_zone = -7

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://businessguysonbusinesstrips.com/?feed=atom')
        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.published_parsed) == self.pub_date:
                self.title = entry.title
                page = self.parse_page(entry.link)
                page.remove('img[src$="/art/wgp_banner.jpg"]')
                self.url = page.src(
                    'img[src^="http://businessguysonbusinesstrips.com/art/"]')
