from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Bunny'
    language = 'en'
    url = 'http://bunny-comic.com/'
    start_date = '2004-08-22'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'H. Davies, CC BY-NC-SA'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.bunny-comic.com/rss/bunny.xml')

        for entry in self.feed.entries:
            title = entry.title
            pieces = entry.summary.split('"')
            for i, piece in enumerate(pieces):
                if piece.count('src='):
                    url = pieces[i + 1]
                    break
            image_name = url.replace('http://bunny-comic.com/strips/', '')
            if self.pub_date == self.string_to_date(image_name[:6], '%d%m%y'):
                self.title = title
                self.url = url
                return
