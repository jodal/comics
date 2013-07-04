from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Orneryboy'
    language = 'en'
    url = 'http://www.orneryboy.com/'
    start_date = '2002-07-22'
    rights = 'Michael Lalonde'


class Crawler(CrawlerBase):
    history_capable_days = 100
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://orneryboy.com/rssfeed.php')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('#comicFlash img')
            title = entry.title
            text = entry.description
            return CrawlerImage(url, title, text)
