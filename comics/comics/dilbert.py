from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dilbert'
    language = 'en'
    url = 'http://www.dilbert.com/'
    start_date = '1989-04-16'
    rights = 'Scott Adams'


class Crawler(CrawlerBase):
    history_capable_date = '1989-04-16'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Mountain'

    def crawl(self, pub_date):
        page = self.parse_page(
            pub_date.strftime('http://dilbert.com/strips/comic/%Y-%m-%d/'))
        url = page.src('img[src$=".strip.zoom.gif"]')
        return CrawlerImage(url)
