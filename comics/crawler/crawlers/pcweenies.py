from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The PC Weenies'
    language = 'en'
    url = 'http://www.pcweenies.net/'
    start_date = '1998-10-21'
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Krishna M. Sadasivam'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://pcweenies.com/feed/')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                self.text = self.remove_html_tags(entry.summary)
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if (piece.count('src=') and
                        pieces[i + 1].startswith(
                            'http://pcweenies.com/comics/')):
                        self.url = pieces[i + 1]
                        return
