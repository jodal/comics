from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Hark, A Vagrant!'
    language = 'en'
    url = 'http://www.harkavagrant.com/'
    start_date = '2008-05-01'
    history_capable_days = 120
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Kate Beaton'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.rsspect.com/rss/vagrant.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img[src*="/history/"]')
            self.title = entry.summary.title('img[src*="/history/"]')
