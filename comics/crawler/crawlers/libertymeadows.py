import re

from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        creators_com_comic_serial = '13'
        self.feed_url = 'http://www.creators.com/comics/liberty-meadows.rss'
        self.parse_feed()

        for entry in self.feed['entries']:
            if self.timestamp_to_date(entry['updated_parsed']) == self.pub_date:
                match = re.match(r'.*/(\d+).html', entry['link'])
                if match is not None:
                    strip_serial = match.groups()[0]
                    self.url = 'http://www.creators.com/comics/%(comic)s/%(strip)s_image.jpg' % {
                        'comic': creators_com_comic_serial,
                        'strip': strip_serial,
                    }
                    return
