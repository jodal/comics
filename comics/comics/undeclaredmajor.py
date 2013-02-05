from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Undeclared Major'
    language = 'en'
    url = 'http://www.undeclaredcomics.com/'
    start_date = '2011-08-09'
    rights = 'Belal'

class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = 'Tu'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.undeclaredcomics.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            url = entry.summary.src('img.comicthumbnail')
            if not url:
                continue
            url = url.replace('comics-rss', 'comics')
            title = entry.title
            return CrawlerImage(url, title)
