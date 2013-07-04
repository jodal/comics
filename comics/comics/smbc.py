from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Saturday Morning Breakfast Cereal'
    language = 'en'
    url = 'http://www.smbc-comics.com/'
    start_date = '2002-09-05'
    rights = 'Zach Weiner'


class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.smbc-comics.com/rss.php')
        for entry in feed.for_date(pub_date):
            url_1 = entry.summary.src('img[src*="/comics/"]')
            url_2 = url_1.replace('.gif', 'after.gif')
            return [CrawlerImage(url_1), CrawlerImage(url_2)]
