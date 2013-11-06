from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Crooked Gremlins'
    language = 'en'
    url = 'http://www.crookedgremlins.com/'
    start_date = '2008-04-01'
    rights = 'Carter Fort and Paul Lucci'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://crookedgremlins.com/feed/')
        for entry in feed.for_date(pub_date):
            if not 'Comics' in entry.tags:
                continue
            title = entry.title
            url = entry.summary.src('img[src*="/comics/"]')

            # Put together the text from multiple paragraphs
            text_paragraphs = entry.summary.text('p', allow_multiple=True)
            if text_paragraphs is not None:
                text = '\n\n'.join(text_paragraphs)
            else:
                text = None

            return CrawlerImage(url, title, text)
