from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Gun Show'
    language = 'en'
    url = 'http://www.gunshowcomic.com/'
    start_date = '2008-09-04'
    rights = '"Lord KC Green"'


class Crawler(CrawlerBase):
    history_capable_date = '2008-09-04'
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page_url = 'http://www.gunshowcomic.com/d/%s.html' % (
            pub_date.strftime('%Y%m%d'),)
        page = self.parse_page(page_url)
        urls = page.src(
            'img[src^="http://gunshowcomic.com/comics/"]', allow_multiple=True)
        return [CrawlerImage(url) for url in urls]
