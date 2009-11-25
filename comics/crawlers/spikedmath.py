from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'Spiked Math'
    language = 'en'
    url = 'http://www.spikedmath.com/'
    start_date = '2009-08-24'
    history_capable_days = 20
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Mike, CC BY-NC-SA 2.5'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://feeds.feedburner.com/SpikedMath')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                self.web_url = entry.link
                if self.title and self.web_url:
                    break

        if not self.web_url:
            return

        page = LxmlParser(self.web_url)
        self.url = page.src('div.asset-body img')
