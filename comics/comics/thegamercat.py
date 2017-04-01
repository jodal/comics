from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'The Gamer Cat'
    language = 'en'
    url = 'http://thegamercat.com/'
    start_date = '2011-06-10'
    rights = 'Celesse'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'US/Central'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed('http://thegamercat.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            if not url:
                continue
            url = url.replace('-200x150', '')
            title = entry.title
            text = '\n\n'.join(entry.content0.text(
                'p', allow_multiple=True)).strip()
            return CrawlerImage(url, title, text)
