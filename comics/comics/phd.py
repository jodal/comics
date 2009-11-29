from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Piled Higher and Deeper'
    language = 'en'
    url = 'http://www.phdcomics.com/'
    start_date = '1997-10-27'
    history_capable_date = '1997-10-27'
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Jorge Cham'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://www.phdcomics.com/gradfeed_justcomics.php')
        for entry in self.feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title.split("'")[1]
