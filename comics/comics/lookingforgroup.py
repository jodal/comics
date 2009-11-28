from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Looking For Group'
    language = 'en'
    url = 'http://lfgcomic.com/'
    start_date = '2006-11-06'
    history_capable_date = '2006-11-06'
    schedule = 'Mo,Th'
    time_zone = -5
    rights = 'Ryan Sohmer & Lar deSouza'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed(
            'http://feeds.feedburner.com/LookingForGroup?format=xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Looking For Group:')):
                self.title = entry.title.replace(
                    'Looking For Group:', '').strip()
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
