from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.bunny-comic.com/rss/bunny.xml')

        for entry in self.feed['entries']:
            title = entry['title']
            pieces = entry['summary'].split('"')
            for i, piece in enumerate(pieces):
                if piece.count('src='):
                    url = pieces[i + 1]
                    break
            image_name = url.replace('http://bunny-comic.com/strips/', '')
            if image_name == 'buffer.jpg':
                continue
            else:
                pub_date = self.string_to_date(image_name[:6], '%d%m%y')
                if pub_date == self.pub_date:
                    self.title = title
                    self.url = url
                    return
