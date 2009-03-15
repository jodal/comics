import re

from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.joyoftech.com/joyoftech/jotblog/atom.xml')

        for entry in self.feed.entries:
            if (re.match('^JoT[ #]*\d.*', entry.title)
                and self.timestamp_to_date(entry.updated_parsed)
                    == self.pub_date):
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and 'alt' in image
                and image['alt'] == 'The Joy of Tech comic'):
                self.url = self.join_web_url(image['src'])
                return
