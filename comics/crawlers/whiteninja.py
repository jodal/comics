from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'White Ninja'
    language = 'en'
    url = 'http://www.whiteninjacomics.com/'
    start_date = '2002-01-01'
    history_capable_days = 60
    time_zone = -6
    rights = 'Scott Bevan & Kent Earle'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.whiteninjacomics.com/rss/z-latest.xml')
        for entry in self.feed.entries:
            if (entry.updated_parsed and
                    self.timestamp_to_date(entry.updated_parsed)
                    == self.pub_date):
                self.title = entry.title.split(' - ')[0]
                page = LxmlParser(entry.link)
                page.remove('img[src*="/images/comics/t-"]')
                self.url = page.src('img[src*="/images/comics/"]')
