from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
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
        feed = self.parse_feed('http://feeds.feedburner.com/ScenesFromAMultiverse')
        for entry in feed.for_date(pub_date):
            description = entry.html(entry.description)
            url = description.src('img[src*="comics-rss"]')
            title = entry.title
            text = ''

            # Text comes in multiple paragraphs: parse out all the text
            all_text = entry.content0.text('p', allow_multiple=True)
            for paragraph in all_text:
                text += paragraph + '\n\n'

            text = text.strip()
            return CrawlerImage(url, title, text)
