from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Three Panel Soul'
    language = 'en'
    url = 'http://www.threepanelsoul.com/'
    start_date = '2006-11-05'
    history_capable_days = 180
    time_zone = -5
    rights = 'Ian McConville & Matt Boyd'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.rsspect.com/rss/threeps.xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                    if piece.count('alt='):
                        self.text = pieces[i + 1]
                    if self.url and self.text:
                        return
