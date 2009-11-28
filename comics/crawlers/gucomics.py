from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'GU Comics'
    language = 'en'
    url = 'http://www.gucomics.com/'
    start_date = '2000-07-10'
    history_capable_date = '2000-07-10'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'Woody Hearn'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.gucomics.com/rss.xml')
        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Comic:')):
                self.title = entry.description
                page = LxmlParser(entry.link)
                self.url = page.src(
                    'img[src^="http://www.gucomics.com/comics/"]'
                    '[alt^="Comic for:"]')
