from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'White Ninja'
    language = 'en'
    url = 'http://www.whiteninjacomics.com/'
    start_date = '2002-01-01'
    rights = 'Scott Bevan & Kent Earle'

class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = 'America/Regina'

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.whiteninjacomics.com/rss/z-latest.xml')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            page.remove('img[src*="/images/comics/t-"]')
            url = page.src('img[src*="/images/comics/"]')
            title = entry.title.split(' - ')[0]
            return CrawlerImage(url, title)
