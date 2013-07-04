from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Ctrl+Alt+Del'
    language = 'en'
    url = 'http://www.cad-comic.com/cad/'
    start_date = '2002-10-23'
    rights = 'Tim Buckley'


class Crawler(CrawlerBase):
    history_capable_date = '2002-10-23'
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

     # Without User-Agent set, the server returns empty responses
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page = self.parse_page(
            'http://www.cad-comic.com/cad/%s' % pub_date.strftime('%Y%m%d'))
        url = page.src('img[src*="/comics/"]')
        title = page.alt('img[src*="/comics/"]')
        return CrawlerImage(url, title)
