from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Something of that Ilk'
    language = 'en'
    url = 'http://www.somethingofthatilk.com/'
    start_date = '2011-02-19'
    rights = 'Ty Devries'

class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page = self.parse_page('http://www.somethingofthatilk.com/')
        url = page.src('img[src*="/comics/"]')
        title = page.alt('img[src*="/comics/"]')
        return CrawlerImage(url, title)
