from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'I Can Barely Draw'
    language = 'en'
    url = 'http://www.icanbarelydraw.com/'
    start_date = '2011-08-05'
    rights = 'Group effort, CC BY-NC-ND 3.0'


class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = 'Mo'
    time_zone = 'US/Pacific'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.icanbarelydraw.com/comic/feed')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[class="comicthumbnail"]')
            if url is None:
                continue
            title = entry.summary.alt('img[class="comicthumbnail"]')
            return CrawlerImage(url, title)
