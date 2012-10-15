from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Geek and Poke'
    language = 'en'
    url = 'http://www.geekandpoke.com/'
    start_date = '2006-08-22'
    rights = 'Oliver Widder, CC BY-ND 2.0'

class Crawler(CrawlerBase):
    history_capable_days = 32
    time_zone = 'Europe/Berlin'

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://geekandpoke.typepad.com/geekandpoke/atom.xml')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img.asset-image')
            title = entry.title
            return CrawlerImage(url, title)
