from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Bizarro'
    language = 'en'
    url = 'http://www.bizarrocomics.com/'
    start_date = '1985-01-01'
    rights = 'Dan Piraro'

class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.bizarrocomics.com/?feed=rss2')

        for entry in feed.for_date(pub_date):
            if 'daily Bizarros' not in entry.tags:
                continue

            urls = entry.content0.src('img.size-full', allow_multiple=True)
            url = urls[0]
            title = entry.title

            # FIXME Store "Bizarro is brought to you today by ..."
            return CrawlerImage(url, title)
