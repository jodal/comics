from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Married To The Sea'
    language = 'en'
    url = 'http://www.marriedtothesea.com/'
    start_date = '2006-02-13'
    rights = 'Drew'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.marriedtothesea.com/rss/rss.php')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src(
                'img[src*="/%s/"]' % pub_date.strftime('%m%d%y'))
            title = entry.title
            return CrawlerImage(url, title)
