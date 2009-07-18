import re

from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Cyanide and Happiness'
    language = 'en'
    url = 'http://www.explosm.net/comics/'
    start_date = '2005-01-26'
    history_capable_days = 7
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Kris Wilson, Rob DenBleyker, Matt Melvin, & Dave McElfatrick '

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://feeds.feedburner.com/Explosm')

        for entry in self.feed.entries:
            if entry.title == self.pub_date.strftime('%m.%d.%Y'):
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and 'alt' in image and
                image['alt'] == 'Cyanide and Happiness, a daily webcomic'):
                #m = re.match('.*/(\w+)\..*', image['src'])
                #self.title = m.groups()[0]
                self.url = image['src']
                break

        p = re.compile('(\d{2}).(\d{2}).(\d{4})\s-\sby.*')
        for tag in self.web_page.tags:
            if 'data' in tag:
                m = p.search(tag['data'])
                if m is not None:
                    m = m.groups()
                    self.pub_date = datetime.date(
                        int(m[2]), int(m[0]), int(m[1]))
                    break

        if not self.pub_date:
            raise StripURLNotFound
