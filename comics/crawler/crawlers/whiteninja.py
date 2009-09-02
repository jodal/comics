from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'White Ninja'
    language = 'en'
    url = 'http://www.whiteninjacomics.com/'
    start_date = '2002-01-01'
    history_capable_days = 15
    time_zone = -6
    rights = 'Scott Bevan & Kent Earle'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.whiteninjacomics.com/rss/z-latest.xml')

        for entry in self.feed.entries:
            if (entry.updated_parsed and
                self.timestamp_to_date(entry.updated_parsed) == self.pub_date):
                self.title = entry.title.split(' - ')[0]
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        page = LxmlParser(self.web_url)
        page.remove('img[src^="http://www.whiteninjacomics.com/images/comics/t-"]')
        self.url = page.src('img[src^="http://www.whiteninjacomics.com/images/comics/"]')
