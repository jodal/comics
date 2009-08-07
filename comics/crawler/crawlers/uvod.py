from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta
from comics.crawler.utils.lxmlparser import LxmlParser

class ComicMeta(BaseComicMeta):
    name = 'The Unspeakable Vault (of Doom)'
    language = 'en'
    url = 'http://www.macguff.fr/goomi/unspeakable/'
    history_capable_days = 180
    time_zone = 1
    rights = 'Francois Launet'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        # FIXME: The uvod feed often contains dates which feedparser fails
        # to parse, like '19 Sept 2008 00:00:00 -0800'

        self.parse_feed('http://www.macguff.fr/goomi/unspeakable/rss.xml')

        for entry in self.feed.entries:
            if (entry.updated_parsed is not None and
                self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Strip #')):
                self.title = entry.summary
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        page = LxmlParser(self.web_url)
        self.url = page.src('img[src*="WEBIMAGES/CARTOON"]')
        self.title = page.text('font[color="#40d265"]', default="")
