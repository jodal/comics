from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Zits'
    language = 'en'
    url = 'http://www.arcamax.com/zits'
    start_date = '1997-07-01'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Tu,Fr,Sa,Su'
    time_zone = -5
    rights = 'Jerry Scott and Jim Borgman'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.arcamax.com/zits/channelfeed')
        for entry in self.feed.entries:
            if entry.title.endswith(self.pub_date.strftime('%-1m/%-1d/%Y')):
                page = self.parse_page(entry.link)
                self.url = page.src('p.m0 img')
