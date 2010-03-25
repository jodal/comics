from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Questionable Content'
    language = 'en'
    url = 'http://questionablecontent.net/'
    start_date = '2003-08-01'
    rights = 'Jeph Jacques'

class Crawler(CrawlerBase):
    history_capable_date = '2003-08-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.questionablecontent.net/QCRSS.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="questionablecontent"]')

            if url is None:
                continue

            title = entry.title
            paragraphs = [p.strip() for p in entry.html(entry.description)
                .text('p', default=[], allow_multiple=True) if p.strip()]
            text = '\n\n'.join(paragraphs)
            return CrawlerImage(url, title, text)
