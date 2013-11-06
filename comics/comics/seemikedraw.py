from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'seemikedraw'
    language = 'en'
    url = 'http://seemikedraw.com.au/'
    start_date = '2007-07-31'
    rights = 'Mike Jacobsen'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'Australia/Sydney'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed('http://seemikedraw.com.au/feed')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
