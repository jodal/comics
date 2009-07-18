from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

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
    def _get_url(self):
        self.parse_feed('http://www.phdcomics.com/gradfeed_justcomics.php')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title.split("'")[1]
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
