from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

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
                page = self.parse_page(entry.link)
                self.url = page.src('div.asset-body img')
