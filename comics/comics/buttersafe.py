from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Buttersafe'
    language = 'en'
    url = 'http://buttersafe.com/'
    start_date = '2007-04-03'
    rights = 'Alex Culang & Raynato Castro'


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'Th'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/Buttersafe?format=xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            if not url:
                continue
            url = url.replace('/rss/', '/').replace('RSS.jpg', '.jpg')
            title = entry.title
            return CrawlerImage(url, title)
