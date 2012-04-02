from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Gamer Cat'
    language = 'en'
    url = 'http://thegamercat.com/'
    start_date = '2011-06-10'
    rights = 'Celesse'

class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://thegamercat.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            url = entry.content0.src('img')
            url = url.replace('/comic-rss/', '/comic/')
            title = entry.title
            text = '\n\n'.join(entry.content0.text(
                'p', allow_multiple=True)).strip()
            return CrawlerImage(url, title, text)
