import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Virtual Shackles'
    language = 'en'
    url = 'http://www.virtualshackles.com/'
    start_date = '2009-03-27'
    rights = 'Jeremy Vinar & Mike Fahmie'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = 'We,Fr'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/VirtualShackles')

        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="virtualshackles.com/img/"]')
            title = entry.title

            page_url = entry.raw_entry.feedburner_origlink
            page_url = re.sub(r'/(\d+/?)', '/-\g<1>', page_url)

            page = self.parse_page(page_url)
            orion = page.text('#orionComments')
            jack = page.text('#jackComments')

            if orion and jack:
                comments = u'orion: %s\n jack: %s' % (orion, jack)
            elif orion:
                comments = u'orion: %s' % (orion)
            elif jack:
                comments = u'jack: %s' % (jack)
            else:
                comments = None

            return CrawlerImage(url, title, comments)
