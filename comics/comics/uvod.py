from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Unspeakable Vault (of Doom)'
    language = 'en'
    url = 'http://www.goominet.com/unspeakable-vault/'
    rights = 'Francois Launet'

class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.goominet.com/unspeakable-vault/'
            '?type=103&ecorss[clear_cache]=1')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            text = entry.summary.text('.bodytext')
            return CrawlerImage(url, title, text)
