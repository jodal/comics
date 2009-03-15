from comics.crawler.crawlers import BaseComicCrawler

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
