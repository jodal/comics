from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Real Life'
    language = 'en'
    url = 'http://www.reallifecomics.com/'
    start_date = '1999-11-15'
    rights = 'Greg Dean'

class Crawler(CrawlerBase):
    history_capable_date = '1999-11-15'

    def crawl(self, pub_date):
        page_url = 'http://www.reallifecomics.com/archive/%s.html' % (
            pub_date.strftime('%y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[alt^="strip for"]')
        return CrawlerImage(url)
