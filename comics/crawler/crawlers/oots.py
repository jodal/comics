from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Order of the Stick'
    language = 'en'
    url = 'http://www.giantitp.com/'
    start_date = '2003-09-30'
    history_capable_days = 1
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Rich Burlew'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.giantitp.com/comics/oots.rss')

        if len(self.feed.entries):
            entry = self.feed.entries[0]
            if 'title' in entry:
                self.title = entry.title
            if 'link' in entry:
                self.web_url = entry.link

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if 'src' in image and image['src'].startswith('/comics/images/'):
                self.url = self.join_web_url(image['src'])
                return
