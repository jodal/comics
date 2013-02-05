from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Bizarro'
    language = 'en'
    url = 'http://bizarrocomics.com/'
    start_date = '1985-01-01'
    rights = 'Dan Piraro'

class Crawler(CrawlerBase):
    history_capable_days = 40
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://bizarrocomics.com/feed/')

        for entry in feed.for_date(pub_date):
            if 'daily Bizarros' not in entry.tags:
                continue

            page = self.parse_page(entry.link)

            results = []
            for url in page.src('img.size-full', allow_multiple=True):
                results.append(CrawlerImage(url))

            if results:
                results[0].title = entry.title
                return results
