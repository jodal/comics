from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'User Friendly'
    language = 'en'
    url = 'http://www.userfriendly.org/'
    start_date = '1997-11-17'
    rights = 'J.D. "Illiad" Frazer'

class Crawler(CrawlerBase):
    history_capable_date = '1997-11-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    has_rerun_releases = True

    def crawl(self, pub_date):
        page_url = 'http://ars.userfriendly.org/cartoons/?id=%s' % (
            pub_date.strftime('%Y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[alt^="Strip for"]')
        return CrawlerImage(url)
