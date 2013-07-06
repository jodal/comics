from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'AmazingSuperPowers'
    language = 'en'
    url = 'http://www.amazingsuperpowers.com/'
    start_date = '2007-09-24'
    rights = 'Wes & Tony'


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feedburner.com/amazingsuperpowers')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img')
            title = entry.title.split(' (')[0]
            text = entry.content0.title('img')
            return CrawlerImage(url, title, text)
