from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sherman's Lagoon"
    language = 'en'
    url = 'http://shermanslagoon.com/'
    start_date = '1991-05-13'
    rights = 'Jim Toomey'


class Crawler(CrawlerBase):
    history_capable_date = '2003-12-29'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page_url = 'http://shermanslagoon.com/comics/%s-%s-%s/' % (
            pub_date.strftime('%B').lower(),
            int(pub_date.strftime('%d')),
            pub_date.strftime('%Y'))
        page = self.parse_page(page_url)
        url = page.src('.entry-content img')
        return CrawlerImage(url)
