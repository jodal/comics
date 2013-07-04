from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dungeons & Denizens'
    language = 'en'
    url = 'http://dungeond.com/'
    start_date = '2005-08-23'
    rights = 'Graveyard Greg'


class Crawler(CrawlerBase):
    history_capable_days = 365
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://dungeond.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            if url:
                url = url.replace('comics-rss', 'comics')
            title = entry.title
            paragraphs = entry.content0.text('p', allow_multiple=True)
            text = '\n\n'.join(paragraphs)
            return CrawlerImage(url, title, text)
