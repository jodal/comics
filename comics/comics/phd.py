from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Piled Higher and Deeper'
    language = 'en'
    url = 'http://www.phdcomics.com/'
    start_date = '1997-10-27'
    history_capable_date = '1997-10-27'
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Jorge Cham'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.phdcomics.com/gradfeed_justcomics.php')
        for entry in self.feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title.split("'")[1]
            return CrawlerResult(url, title)
