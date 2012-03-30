from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Scenes from a Multiverse'
    language = 'en'
    url = 'http://amultiverse.com/'
    start_date = '2010-06-14'
    rights = 'Jonathan Rosenberg'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -4

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/ScenesFromAMultiverse')

        for entry in feed.for_date(pub_date):
            description = entry.html(entry.description)
            url = description.src('img[src*="comics-rss"]')
            title = entry.title

            # Text comes in multiple paragraphs: parse out all the text
            text = ''
            for paragraph in entry.content0.text('p', allow_multiple=True):
                text += paragraph + '\n\n'
            text = text.strip()

            return CrawlerImage(url, title, text)
