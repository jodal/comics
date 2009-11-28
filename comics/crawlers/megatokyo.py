from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

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
                and entry.title.startswith('Comic [')):
                self.title = entry.title.split('"')[1]
                page = LxmlParser(entry.link)
                self.url = page.src('img[src^="http://megatokyo.com/strips/"]')
