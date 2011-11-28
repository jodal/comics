from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Manly Guys Doing Manly Things'
    language = 'en'
    url = 'http://thepunchlineismachismo.com/'
    start_date = '2005-05-29'
    rights = 'Kelly Turnbull, CC BY-NC-SA 3.0'

class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = 'Mo'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://thepunchlineismachismo.com/feed')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics-rss/"]')
HEAD
            title = entry.title 
            return CrawlerImage(url, title)

=======
            title = entry.title
            return CrawlerImage(url, title)
>>>>>>> 6ac330d33c43958d02d55072544ca473255a1218
