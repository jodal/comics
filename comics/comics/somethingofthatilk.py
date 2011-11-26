from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Something of that ilk'
    language = 'en'
    url = 'http://somethingofthatilk.com/'
    start_date = '2011-02-19'
    rights = 'Ty Devries'

class Crawler(CrawlerBase):
    history_capable_date = '2011-02-19'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://somethingofthatilk.com/rss/index.php')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
