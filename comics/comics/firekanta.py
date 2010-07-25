from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Firekanta'
    language = 'no'
    url = 'http://www.kantenstrek.no/galleri/firekanta'
    start_date = '2004-03-01'
    rights = 'Kanten Strek'

class Crawler(CrawlerBase):
    # There's a very erratic publishing history in the feed, so there's never a
    # static number of days to get history.  I'm, therefore, going to put in a
    # static value that goes a long ways back.  This will limit excessive
    # crawling, though provide for what is likely to be the entire history.
    history_capable_days = 90
    time_zone = 2

    def crawl(self, pub_date):

        feed = self.parse_feed('http://www.kantenstrek.no/feed')
        for entry in feed.for_date(pub_date):
	    # This guy releases a few comics in the same feed, look
	    # specifically for Firekanta...
            if 'Firekanta' not in entry.title:
                continue

            title = entry.title

            page_uri = entry.link
            page_html = self.parse_page(page_uri)
            img_url = page_html.src('div[class="post"] img[src*="/wp-content/"]')

            if img_url is not None:
                return CrawlerImage(img_url, title)
