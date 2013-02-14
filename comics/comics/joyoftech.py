from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'The Joy of Tech'
    language = 'en'
    url = 'http://www.geekculture.com/joyoftech/'
    start_date = '2000-08-14'
    rights = 'Geek Culture'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.joyoftech.com/joyoftech/jotblog/atom.xml')
        for entry in feed.for_date(pub_date):
            title = entry.title
            if not title.startswith('JoT'):
                continue
            url = entry.content0.src('img')
            if url:
                url = url.replace('superthumb', '')
            return CrawlerImage(url, title)
