from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Red meat'
    language = 'en'
    url = 'http://www.redmeat.com/'
    start_date = '1996-06-10'
    rights = 'Max Cannon'


class Crawler(CrawlerBase):
    history_capable_date = '1996-06-10'
    schedule = 'Tu'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page_url = 'http://www.redmeat.com/redmeat/%s/index.html' % (
            pub_date.strftime('%Y-%m-%d'))

        page = self.parse_page(page_url)

        url = page.src('img', allow_multiple=True)[0]
        title = page.alt('img', allow_multiple=True)[0]

        return CrawlerImage(url, title)
