from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Scenes from a Multiverse'
    language = 'en'
    url = 'http://amultiverse.com/'
    start_date = '2010-06-14'
    rights = 'Jonathan Rosenberg'


class Crawler(CrawlerBase):
    history_capable_days = 40
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://amultiverse.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('a[rel="bookmark"] img')
            title = entry.title

            # Text comes in multiple paragraphs: parse out all the text
            text = ''
            for paragraph in entry.content0.text('p', allow_multiple=True):
                text += paragraph + '\n\n'
            text = text.strip()

            return CrawlerImage(url, title, text)
