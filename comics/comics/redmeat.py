from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Red Meat'
    language = 'en'
    url = 'http://www.redmeat.com/'
    start_date = '1996-06-10'
    rights = 'Max Cannon'


class Crawler(CrawlerBase):
    history_capable_date = '1996-06-10'
    schedule = 'Tu'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page_url = 'http://www.redmeat.com/redmeat/%s/' % (
            pub_date.strftime('%Y-%m-%d'))
        page = self.parse_page(page_url)
        url = page.src('#weeklyStrip img')
        title = page.alt('#weeklyStrip img')
        return CrawlerImage(url, title)
