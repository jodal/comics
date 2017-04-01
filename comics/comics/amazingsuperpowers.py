from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'AmazingSuperPowers'
    language = 'en'
    url = 'http://www.amazingsuperpowers.com/'
    start_date = '2007-09-24'
    rights = 'Wes & Tony'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Th'
    time_zone = 'US/Eastern'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/amazingsuperpowers')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.content0.title('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
