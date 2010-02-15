from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Wondermark'
    language = 'en'
    url = 'http://wondermark.com/'
    start_date = '2003-04-25'
    rights = 'David Malki'

class Crawler(CrawlerBase):
    history_capable_days = 28
    schedule = 'Tu,Fr'
    time_zone = -8 

    def crawl(self, pub_date):
        feed_url = 'http://feeds.feedburner.com/wondermark'
        feed = self.parse_feed( feed_url )
        for entry in feed.for_date( pub_date ):
            url=entry.content0.src( r'img[src*="/c/"]' )
            title=entry.title
            text=entry.content0.alt( r'img[src*="/c/"]' )
            # Some of these content blocks are blog posts, not just comics, and David overlaps them with posts.  Argh.
            if url != None:
                    return CrawlerImage(url, title=title, text=text)
