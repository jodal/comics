from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Count Your Sheep'
    language = 'en'
    url = 'http://www.countyoursheep.com/'
    start_date = '2003-06-11'
    rights = 'Adrian "Adis" Ramos'

class Crawler(CrawlerBase):
    history_capable_date = '2003-06-11'
    schedule = None

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page_url = 'http://countyoursheep.keenspot.com/d/%s.html' % (
            pub_date.strftime('%Y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[src^="http://cdn.countyoursheep.keenspot.com/comics/"]')
        return CrawlerImage(url)
