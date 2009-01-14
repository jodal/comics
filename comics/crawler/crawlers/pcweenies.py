from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.feed_url = 'http://pcweenies.com/feed/'
        self.parse_feed()

        for entry in self.feed['entries']:
            if self.timestamp_to_date(entry['updated_parsed']) == self.pub_date:
                self.title = entry['title']
                self.text = self.remove_html_tags(entry['summary'])
                pieces = entry['summary'].split('"')
                for i, piece in enumerate(pieces):
                    if (piece.count('src=') and
                        pieces[i + 1].startswith('http://pcweenies.com/comics/')):
                        self.url = pieces[i + 1]
                        return
