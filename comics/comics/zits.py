from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Zits'
    language = 'en'
    url = 'http://www.arcamax.com/zits'
    start_date = '1997-07-01'
    rights = 'Jerry Scott and Jim Borgman'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.arcamax.com/thefunnies/zits/rss')
        for entry in feed.all():
            if entry.title.endswith(pub_date.strftime('%-1m/%-1d/%Y')):
                url = entry.summary.src('img')
                return CrawlerImage(url)
