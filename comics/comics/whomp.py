from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase
import re
import datetime

class ComicData(ComicDataBase):
    name = 'Whomp!'
    language = 'en'
    url = 'http://www.whompcomic.com/'
    start_date = '2010-06-14'
    rights = 'Ronnie Filyaw'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.whompcomic.com/feed/rss/')

        for entry in feed.all():
            url = entry.summary.src('img[src*="/comics-rss/"]')
            if not url:
                continue

            title = entry.title
            url = url.replace('comics-rss', 'comics')
            text = entry.summary.alt('img[src*="/comics-rss/"]').encode('utf-8','ignore')

            # extract date from url, since we don't have this in the xml
            match = re.search(r'comics/(\d{4}-\d{2}-\d{2})', url)
            if match:
                comic_date = datetime.datetime.strptime(match.group(1), '%Y-%m-%d')

                if pub_date.day == comic_date.day and pub_date.month == comic_date.month and pub_date.year == comic_date.year:
                    return CrawlerImage(url, title, text)
