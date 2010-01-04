from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Bizarro'
    language = 'en'
    url = 'http://bizarrocomic.blogspot.com/'
    start_date = '1985-01-01'
    rights = 'Dan Piraro'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/bizarroblog')

        for entry in feed.for_date(pub_date):
            if 'daily Bizarros' not in entry.tags:
                continue

            # We want direct link to image, not an HTML page.
            url = entry.summary.href('a:first-child')
            url = url.replace('s1600-h', 's1600')

            title = entry.title

            # FIXME Store "Bizarro is brought to you today by ..."
            return CrawlerResult(url, title)
