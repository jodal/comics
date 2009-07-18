from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'GU Comics'
    language = 'en'
    url = 'http://www.gucomics.com/'
    start_date = '2000-07-10'
    history_capable_date = '2000-07-10'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'Woody Hearn'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.gucomics.com/rss.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Comic:')):
                self.title = entry.description
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and image['src'].startswith('/comics/')
                and 'alt' in image
                and image['alt'].startswith('Comic for:')):
                self.url = self.join_web_url(image['src'])
                break
