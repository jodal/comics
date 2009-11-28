import re

from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Liberty Meadows'
    language = 'en'
    url = 'http://www.creators.com/comics/liberty-meadows.html'
    start_date = '1997-03-30'
    end_date = '2001-12-31'
    history_capable_days = 19
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Frank Cho'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        creators_com_comic_serial = '13'
        self.parse_feed('http://www.creators.com/comics/liberty-meadows.rss')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                match = re.match(r'.*/(\d+).html', entry.link)
                if match is not None:
                    strip_serial = match.groups()[0]
                    self.url = 'http://www.creators.com/comics/%(comic)s/%(strip)s_image.gif' % {
                        'comic': creators_com_comic_serial,
                        'strip': strip_serial,
                    }
                    return
