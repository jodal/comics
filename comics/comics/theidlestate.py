from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Idle State'
    language = 'en'
    url = 'http://www.theidlestate.com/'
    start_date = '2011-07-18'
    rights = 'Nick Wright'

class Crawler(CrawlerBase):
    history_capable_days = 40
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.theidlestate.com/?feed=rss2')
        for entry in feed.for_date(pub_date):
            if 'Peached' not in entry.tags:
                continue
            url = entry.content0.src('img[src*="/wp-content/webcomic/"]')
            if not url:
                continue
            url = url.replace('/thumbs', '')
            url = url.replace('-medium', '')
            title = entry.title
            return CrawlerImage(url, title)
