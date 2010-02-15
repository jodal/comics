from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'HijiNKS Ensue'
    language = 'en'
    url = 'http://hijinksensue.com/'
    start_date = '2007-05-11'
    rights = 'Joel Watson'

class Crawler(CrawlerBase):
    history_capable_days = 28
    schedule = 'Mo,We,Fr'
    time_zone = 0 

    def crawl(self, pub_date):
        feed_url = 'http://feeds.feedburner.com/hijinksensue'
        feed = self.parse_feed( feed_url )
        for entry in feed.for_date( pub_date ):
            url=entry.content0.src( 'img[src*="/comics/%s"]' % pub_date.strftime( "%Y" ) )
            title=entry.title
            # Weed out the blog posts without images
            if url != None:
                return CrawlerImage(url, title=title)

        # Return an empty crawler image if we can't find anything
        return CrawlerImage( None )
