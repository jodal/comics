from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Yehuda Moon'
    language = 'en'
    url = 'http://www.yehudamoon.com/'
    start_date = '2008-01-22'
    rights = 'Rick Smith'


class Crawler(CrawlerBase):
    history_capable_date = '2008-01-22'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page_url = 'http://www.yehudamoon.com/%s/' % (
            pub_date.strftime('%m%d%Y'),)
        page = self.parse_page(page_url)
        url = page.src('#comic img')
        title = page.alt('#comic img')
        title = title.split(' ', 2)[-1]
        return CrawlerImage(url, title)
