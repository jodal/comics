import re

from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.feed_url = 'http://osnews.com/files/comics.xml'
        self.parse_feed()

        for entry in self.feed['entries']:
            if self.timestamp_to_date(entry['updated_parsed']) == self.pub_date:
                self.title = entry['title']
                m = re.match('.*src="([^"]+)".*', entry['summary'])
                m = m.groups()
                self.url = m[0]
                return
