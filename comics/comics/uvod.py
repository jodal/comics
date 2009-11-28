from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Unspeakable Vault (of Doom)'
    language = 'en'
    url = 'http://www.macguff.fr/goomi/unspeakable/'
    history_capable_days = 180
    time_zone = 1
    rights = 'Francois Launet'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        # FIXME: The uvod feed often contains dates which feedparser fails
        # to parse, like '19 Sept 2008 00:00:00 -0800'

        self.parse_feed('http://www.macguff.fr/goomi/unspeakable/rss.xml')

        for entry in self.feed.entries:
            if (entry.updated_parsed is not None and
                self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Strip #')):
                self.title = entry.summary
                pieces = entry.content[0].value.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
