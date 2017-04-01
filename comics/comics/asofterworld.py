from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'A Softer World'
    language = 'en'
    url = 'http://www.asofterworld.com/'
    start_date = '2003-02-07'
    rights = 'Joey Comeau, Emily Horne'


class Crawler(CrawlerBase):
    schedule = None
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        page = self.parse_page('http://www.asofterworld.com/')
        url = page.src('#comicimg img')
        text = page.title('#comicimg img')
        return CrawlerImage(url, None, text)
