from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

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
    def crawl(self):
        self.parse_feed('http://feeds.feedburner.com/Explosm')
        for entry in self.feed.entries:
            if entry.title == self.pub_date.strftime('%m.%d.%Y'):
                page = self.parse_page(entry.link)
                self.url = page.src(
                    'img[alt="Cyanide and Happiness, a daily webcomic"]')
