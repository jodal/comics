import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'A Softer World'
    language = 'en'
    url = 'http://www.asofterworld.com/'
    start_date = '2003-02-07'
    rights = 'Joey Comeau, Emily Horne'


class Crawler(CrawlerBase):
    history_capable_date = '2003-02-07'
    schedule = None
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        page = self.parse_page('http://www.asofterworld.com/')
        url = page.src('#thecomic img')
        asw_id = re.findall('(\d+).jpg$', url)[0]
        title = 'A Softer World: %s' % asw_id
        text = page.title('#thecomic img')
        return CrawlerImage(url, title, text)
