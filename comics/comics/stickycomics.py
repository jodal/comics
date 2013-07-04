from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Sticky Comics'
    language = 'en'
    url = 'http://www.stickycomics.com/'
    start_date = '2006-05-04'
    rights = 'Christiann MacAuley'


class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = 'US/Mountain'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.stickycomics.com/feed')
        for entry in feed.for_date(pub_date):
            if 'comics' not in entry.tags:
                continue
            url = entry.content0.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            text = entry.content0.alt('img[src*="/wp-content/uploads/"]')
            return CrawlerImage(url, title, text)
