from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Space Avalanche'
    language = 'en'
    url = 'http://www.spaceavalanche.com/'
    start_date = '2009-02-02'
    rights = 'Eoin Ryan'


class Crawler(CrawlerBase):
    history_capable_days = 365
    time_zone = 'Europe/Dublin'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/SpaceAvalanche')
        for entry in feed.for_date(pub_date):
            if 'COMIC ARCHIVE' not in entry.tags:
                continue
            urls = entry.content0.src(
                'img[src*="/wp-content/uploads/"]', allow_multiple=True)
            if not urls:
                continue
            url = urls[0]
            title = entry.title
            return CrawlerImage(url, title)
