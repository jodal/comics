from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Scandinavia and the World'
    language = 'en'
    url = 'http://www.satwcomic.com/'
    start_date = '2009-06-01'
    rights = 'Humon'


class Crawler(CrawlerBase):
    schedule = 'We'
    time_zone = 'Europe/Copenhagen'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/satwcomic')
        for entry in feed.all():
            page = self.parse_page(entry.link)
            url = page.src('.comicmid img[src*="/art/"]')
            title = entry.title
            page.remove('.comicdesc .stand_high h1')
            page.remove('.comicdesc .stand_high small')
            text = page.text('.comicdesc .stand_high').strip()
            return CrawlerImage(url, title, text)
