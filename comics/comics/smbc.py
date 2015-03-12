from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Saturday Morning Breakfast Cereal'
    language = 'en'
    url = 'http://www.smbc-comics.com/'
    start_date = '2002-09-05'
    rights = 'Zach Weiner'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.smbc-comics.com/rss.php')
        for entry in feed.for_date(pub_date):
            title = entry.title.replace(
                'Saturday Morning Breakfast Cereal - ', '')

            url_1 = entry.summary.src('img[src*="/comics/"]')

            page = self.parse_page(entry.link)
            url_2 = page.src('#aftercomic img')

            return [CrawlerImage(url_1, title), CrawlerImage(url_2)]
