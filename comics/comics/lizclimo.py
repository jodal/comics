from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hi, I'm Liz"
    language = 'en'
    url = 'http://lizclimo.tumblr.com/'
    start_date = '2011-12-15'
    rights = 'Liz Climo'


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://lizclimo.tumblr.com/rss')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            if not url:
                continue
            url = url.replace('_500.jpg', '_1280.jpg')
            title = entry.title
            return CrawlerImage(url, title)
