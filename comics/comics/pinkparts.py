from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pink Parts'
    language = 'en'
    url = 'http://pinkpartscomic.com/'
    start_date = '2010-02-01'
    rights = 'Katherine Skipper'


class Crawler(CrawlerBase):
    history_capable_date = '2010-02-01'
    schedule = None
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://pinkpartscomic.com/inc/feed.php')
        for entry in feed.for_date(pub_date):
            url = entry.sunnary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
