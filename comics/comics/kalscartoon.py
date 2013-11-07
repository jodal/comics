from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "KAL's Cartoon"
    language = 'en'
    url = 'http://www.economist.com/'
    start_date = '2006-01-05'
    rights = 'Kevin Kallaugher'


class Crawler(CrawlerBase):
    history_capable_days = 7
    schedule = 'Sa'
    time_zone = 'Europe/London'

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page = self.parse_page('http://www.economist.com/content/kallery')
        url = page.src('.content-image-full img')
        date = pub_date.strftime('%Y%m%d')
        if date in url:
            return CrawlerImage(url)
