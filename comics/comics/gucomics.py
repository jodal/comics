from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'GU Comics'
    language = 'en'
    url = 'http://www.gucomics.com/'
    start_date = '2000-07-10'
    history_capable_date = '2000-07-10'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'Woody Hearn'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.gucomics.com/rss.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Comic:'):
                page = self.parse_page(entry.link)
                url = page.src(
                    'img[src^="http://www.gucomics.com/comics/"]'
                    '[alt^="Comic for:"]')
                title = entry.summary.text('')
                return CrawlerResult(url, title)
