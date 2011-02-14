from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'pictures for sad children'
    language = 'en'
    url = 'http://picturesforsadchildren.com/'
    start_date = '2007-01-01'
    rights = 'John Campbell'

class Crawler(CrawlerBase):
    history_capable_days = 40
    schedule = 'Mo'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.rsspect.com/rss/pfsc.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            return CrawlerImage(url, title)
