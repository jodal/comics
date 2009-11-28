# encoding: utf-8

from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Kukuburi'
    language = 'en'
    url = 'http://www.kukuburi.com/'
    start_date = '2007-09-08'
    history_capable_days = 60
    schedule = 'Tu,Th'
    time_zone = -8
    rights = 'Ramón Pérez'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://feeds2.feedburner.com/Kukuburi')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if (piece.count('src=') and pieces[i + 1].startswith(
                            'http://www.kukuburi.com/v2/comics/')):
                        self.url = pieces[i + 1]
                        return
