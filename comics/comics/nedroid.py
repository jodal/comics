from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Nedroid'
    language = 'en'
    url = 'http://www.nedroid.com/'
    start_date = '2006-04-24'
    rights = 'Anthony Clark'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'US/Eastern'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed('http://nedroid.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comic' not in entry.tags:
                continue
            url = entry.summary.src('img')
            if url is None:
                continue
            url = url.replace('/comic/comics-rss/', '/comics/')
            title = entry.title
            text = entry.summary.title('img')
            return CrawlerImage(url, title, text)
