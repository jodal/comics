from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Blaster Nation'
    language = 'en'
    url = 'http://www.blasternation.com/'
    start_date = '2011-01-27'
    rights = 'Leslie Brown & Brad Brown'


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'We,Fr,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.blasternation.com/rss.php')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img#comic')
            title = entry.title.replace('Blasternation - ', '')
            return CrawlerImage(url, title)
