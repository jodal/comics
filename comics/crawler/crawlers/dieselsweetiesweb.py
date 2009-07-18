from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Diesel Sweeties (web)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2000-01-01'
    history_capable_date = '2000-01-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5
    rights = 'Richard Stevens'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.dieselsweeties.com/ds-unifeed.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('DS Web:')):
                self.title = entry.title.replace('DS Web: ', '').strip()
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                    if piece.count('alt='):
                        self.text = pieces[i + 1]
                    if self.url and self.text:
                        return
