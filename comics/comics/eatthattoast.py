import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Eat That Toast!'
    language = 'en'
    url = 'http://eatthattoast.com/'
    start_date = '2010-06-14'
    rights = 'Matt Czapiewski'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page = self.parse_page('http://eatthattoast.com/')
        url = page.src('#comic img')
        title = page.text('.comicpress_comic_title_widget a')
        text = page.alt('#comic img')
        matches = re.match(r'.*(\d{4}-\d{2}-\d{2}).*', url)
        if matches and matches.groups()[0] == pub_date.isoformat():
            return CrawlerImage(url, title, text)
