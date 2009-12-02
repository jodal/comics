from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Cyanide and Happiness'
    language = 'en'
    url = 'http://www.explosm.net/comics/'
    start_date = '2005-01-26'
    history_capable_days = 7
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Kris Wilson, Rob DenBleyker, Matt Melvin, & Dave McElfatrick '

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/Explosm')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src(
                'img[alt="Cyanide and Happiness, a daily webcomic"]')
            return CrawlerResult(url)
