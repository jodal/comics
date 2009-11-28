from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'pictures for sad children'
    language = 'en'
    url = 'http://picturesforsadchildren.com/'
    start_date = '2007-01-01'
    history_capable_days = 40
    time_zone = -6
    rights = 'John Campbell'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.rsspect.com/rss/pfsc.xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
