from comics.crawler.crawlers import BaseComicCrawler

# XXX Not in use. The comic has multiple strips per date, which we do not
# support.

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://apelad.blogspot.com/feeds/posts/default')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Laugh-Out-Loud Cats #')):
                self.title = entry.title.replace('Laugh-Out-Loud Cats ', '')
                pieces = entry.content.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
