from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Devil Bear'
    language = 'en'
    url = 'http://www.thedevilbear.com/'
    start_date = '2009-01-01'
    history_capable_days = 0
    schedule = 'Mo'
    time_zone = -8
    rights = 'Ben Bourbon'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        page = self.parse_page('http://www.thedevilbear.com/')
        self.url = page.src('#cg_img img')
