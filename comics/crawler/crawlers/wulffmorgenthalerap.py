import re

from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Wulffmorgenthaler (ap.no)'
    language = 'no'
    url = 'http://www.aftenposten.no/tegneserier/'
    start_date = '2001-01-01'
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Mikael Wulff & Anders Morgenthaler'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed(
            'http://www.aftenposten.no/eksport/rss-1_0/'
            '?seksjon=tegneserier&utvalg=siste')

        # XXX: All entries in the feed got the same date, so we just check the
        # first one, and let the later checksumming of the strip image take
        # care of duplicates.
        for entry in self.feed.entries:
            if entry.title == 'Dagens Wulffmorgenthaler':
               self.web_url = entry.link
               break

        if self.web_url is None:
            return

        self.parse_web_page()

        strip_pattern = re.compile(
            r'.*/_(Escenic-)*[Ww]t_\w+_\d{1,2}_\d{6,7}x.jpg$')
        for image in self.web_page.imgs:
            if 'src' in image:
                matches = strip_pattern.match(image['src'])
                if matches is not None:
                    self.url = self.join_web_url(image['src'])
                    return
