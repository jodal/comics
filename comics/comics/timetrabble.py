from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Time Trabble'
    language = 'en'
    url = 'http://timetrabble.com/'
    start_date = '2010-05-09'
    rights = 'Mikey Heller'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://timetrabble.com/?feed=rss2')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img.comicthumbnail')
            if not url:
                continue
            url = url.replace('comics-rss', 'comics')
            title = entry.title
            return CrawlerImage(url, title)
