from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Mystic Revolution'
    language = 'en'
    url = 'http://mysticrevolution.keenspot.com/'
    start_date = '2004-01-01'
    rights = 'Jennifer Brazas'


class Crawler(CrawlerBase):
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'US/Pacific'

     # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page = self.parse_page('http://mysticrevolution.keenspot.com/')
        url = page.src('img[class="ksc"]')
        title = page.alt('img[class="ksc"]')
        return CrawlerImage(url, title)
