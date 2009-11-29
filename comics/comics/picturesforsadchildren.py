from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'pictures for sad children'
    language = 'en'
    url = 'http://picturesforsadchildren.com/'
    start_date = '2007-01-01'
    history_capable_days = 40
    time_zone = -6
    rights = 'John Campbell'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.rsspect.com/rss/pfsc.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img[src*="/comics/"]')
            self.title = entry.title
