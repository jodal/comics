from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Wyyrd'
    language = 'no'
    url = 'http://wyyrd.nettserier.no/'
    start_date = '2008-01-14'
    rights = 'Gard Robot Helset'


class Crawler(CrawlerBase):
    history_capable_date = '2008-01-14'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://wyyrd.nettserier.no/_striper/wyyrd-%s.png' % (
            self.date_to_epoch(pub_date),)
        page_url = 'http://wyyrd.nettserier.no/%s' % (
            pub_date.strftime('%Y/%m/%d'))
        page = self.parse_page(page_url)
        title = page.alt('img[src*="/_striper/"]')
        return CrawlerImage(url, title)
