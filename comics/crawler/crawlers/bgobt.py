from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

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
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image
                and image['src'].startswith(
                    'http://businessguysonbusinesstrips.com/art/')
                and not image['src'].endswith('/art/wgp_banner.jpg')):
                self.url = self.join_web_url(image['src'])
                return
