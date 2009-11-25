from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dueling Analogs'
    language = 'en'
    url = 'http://www.duelinganalogs.com/'
    start_date = '2005-11-17'
    history_capable_days = 35
    schedule = 'Mo,Th'
    time_zone = -7
    rights = 'Steve Napierski'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed(
            'http://feeds2.feedburner.com/DuelingAnalogs?format=xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if (piece.count('src=')
                        and pieces[i + 1].startswith(
                            'http://www.duelinganalogs.com/comics/')):
                        self.url = pieces[i + 1]
                        return
