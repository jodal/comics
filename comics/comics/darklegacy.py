from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dark Legacy'
    language = 'en'
    url = 'http://www.darklegacycomics.com/'
    start_date = '2006-01-01'
    history_capable_date = '2006-12-09'
    schedule = 'Su'
    time_zone = -6
    rights = 'Arad Kedar'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.parse_feed('http://www.darklegacycomics.com/feed.xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                self.url = entry.link.replace('.html', '.jpg')
                return
