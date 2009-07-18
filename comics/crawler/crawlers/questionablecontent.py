from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Questionable Content'
    language = 'en'
    url = 'http://questionablecontent.net/'
    start_date = '2003-08-01'
    history_capable_date = '2003-08-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6
    rights = 'Jeph Jacques'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.questionablecontent.net/QCRSS.xml')

        for entry in self.feed.entries:
            if ('updated_parsed' in entry and
                self.timestamp_to_date(entry.updated_parsed) == self.pub_date):
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
