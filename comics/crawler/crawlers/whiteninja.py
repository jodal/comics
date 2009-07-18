from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'White Ninja'
    language = 'en'
    url = 'http://www.whiteninjacomics.com/'
    start_date = '2002-01-01'
    history_capable_days = 15
    time_zone = -6
    rights = 'Scott Bevan & Kent Earle'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.whiteninjacomics.com/rss/z-latest.xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title.split(' - ')[0]
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and image['src'].startswith('/images/comics/')
                and not image['src'].startswith('/images/comics/t-')):
                self.url = self.join_web_url(image['src'])
                return
