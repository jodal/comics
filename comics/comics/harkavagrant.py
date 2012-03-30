from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Hark, A Vagrant!'
    language = 'en'
    url = 'http://www.harkavagrant.com/'
    start_date = '2008-05-01'
    rights = 'Kate Beaton'

class Crawler(CrawlerBase):
    history_capable_days = 120
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/vagrant.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/history/"]')
            title = entry.summary.title('img[src*="/history/"]')
            return CrawlerImage(url, title)
