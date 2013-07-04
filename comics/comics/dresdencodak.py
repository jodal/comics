from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dresden Codak'
    language = 'en'
    url = 'http://www.dresdencodak.com/'
    start_date = '2007-02-08'
    rights = 'Aaron Diaz'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/rsspect/fJur')
        for entry in feed.for_date(pub_date):
            if 'Comics' in entry.tags:
                page = self.parse_page(entry.link)
                url = page.src('#comic img')
                title = entry.title

                text = ''
                for paragraph in entry.content0.text('p', allow_multiple=True):
                    text += paragraph + '\n\n'
                text = text.strip()

                return CrawlerImage(url, title, text)
