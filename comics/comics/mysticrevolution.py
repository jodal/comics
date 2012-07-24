from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Mystic Revolution'
    language = 'en'
    url = 'http://mysticrevolution.keenspot.com/'
    start_date = '2004-01-01'
    rights = 'Jennifer Brazas'

class Crawler(CrawlerBase):
    history_capable_days = 7
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page = self.parse_page('http://mysticrevolution.keenspot.com/')
        url = page.src('#comicpage_ img')
        title = page.alt('#comicpage_ img')
        if url and pub_date.strftime('%Y%m%d') in url:
            return CrawlerImage(url, title)
