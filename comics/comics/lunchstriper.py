from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.lunch import Meta as LunchMeta

class Meta(LunchMeta):
    name = 'Lunch (lunchstriper.lunddesign.no)'
    url = 'http://lunchstriper.lunddesign.no/'

class Crawler(CrawlerBase):
    time_zone = 1
    history_capable_days = 21

    def crawl(self, pub_date):
        feed = self.parse_feed('http://lunchstriper.lunddesign.no/?feed=rss2')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            return CrawlerImage(url)

