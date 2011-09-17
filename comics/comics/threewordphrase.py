from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Three Word Phrase'
    language = 'en'
    url = 'http://www.threewordphrase.com/'
    start_date = '2010-07-13'
    rights = 'Ryan Pequin'

class Crawler(CrawlerBase):
    history_capable_days = 0

    def crawl(self, pub_date):
        # Thee feed has broken dates, so we fetch only the latest one
        feed = self.parse_feed('http://www.threewordphrase.com/rss.xml')
        entry = feed.all()[0]
        url = entry.link.replace('.htm', '.gif')
        title = entry.title
        text = entry.summary.text('')
        return CrawlerImage(url, title, text)
