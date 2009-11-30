from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Bunny'
    language = 'en'
    url = 'http://bunny-comic.com/'
    start_date = '2004-08-22'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'H. Davies, CC BY-NC-SA'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.bunny-comic.com/rss/bunny.xml')
        for entry in feed.all():
            image_name = entry.summary.src('img[src*="/strips/"]').replace(
                'http://bunny-comic.com/strips/', '')
            if (image_name[:6].isdigit()
                    and self.pub_date == self.string_to_date(
                    image_name[:6], '%d%m%y')):
                self.url = entry.summary.src('img[src*="/strips/"]')
                self.title = entry.title
                self.text = entry.summary.alt('img[src*="/strips/"]')
