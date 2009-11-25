from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

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

        page = LxmlParser(self.web_url)
        page.remove('img[src$="/art/wgp_banner.jpg"]')
        self.url = page.src('img[src^="http://businessguysonbusinesstrips.com/art/"]')
