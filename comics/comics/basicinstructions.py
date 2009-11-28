from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Basic Instructions'
    language = 'en'
    url = 'http://www.basicinstructions.net/'
    start_date = '2006-07-01'
    history_capable_days = 100
    schedule = 'We,Su'
    time_zone = -7
    rights = 'Scott Meyer'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.basicinstructions.net/atom.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('How to')):
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        break
