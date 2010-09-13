from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Stuff No One Told Me'
    language = 'en'
    url = 'http://stuffnoonetoldme.blogspot.com/'
    start_date = '2010-05-31'
    rights = 'Alex Noriega'

class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/StuffNoOneToldMeButILearnedAnyway')
        for entry in feed.for_date(pub_date):
            sequence_number = entry.title.strip().split(' ')[0]
            if not sequence_number.isdigit():
                continue
            urls = entry.content0.href('a[href$="%s.jpg"]' % sequence_number,
                allow_multiple=True)
            result = [CrawlerImage(url) for url in urls]
            if result:
                result[0].title = entry.title
            return result
