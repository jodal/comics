from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'MegaTokyo'
    language = 'en'
    url = 'http://www.megatokyo.com/'
    start_date = '2000-08-14'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Fred Gallagher & Rodney Caston'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.megatokyo.com/rss/megatokyo.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Comic ')):
                self.title = entry.title.split('"')[1]
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if 'src' in image and image['src'].startswith('strips/'):
                self.web_url = 'http://www.megatokyo.com/'
                self.url = self.join_web_url(image['src'])
                return
