from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'The Perry Bible Fellowship'
    language = 'en'
    url = 'http://www.pbfcomics.com/'
    start_date = '2001-01-01'
    history_capable_days = 1
    time_zone = -5
    rights = 'Nicholas Gurewitch'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://pbfcomics.com/feed/feed.xml')

        for entry in self.feed.entries:
            if entry.summary == 'Comic':
                # The feed contains no dates, so we just fetch the first comic
                # entry we find
                self.title = entry.title
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        page = LxmlParser(self.web_url)
        self.url = page.src('img#topimg')
