from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Teh Gladiators'
    language = 'en'
    url = 'http://www.tehgladiators.com/'
    start_date = '2008-03-18'
    rights = 'Uros Jojic & Borislav Grabovic'

class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'Su'
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.tehgladiators.com/rss.xml')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[alt^="Teh Gladiators Webcomic"]')
            title = entry.title
            return CrawlerImage(url, title)
