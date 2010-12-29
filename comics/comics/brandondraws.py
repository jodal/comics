import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase
from HTMLParser import HTMLParser

class Meta(MetaBase):
    name = 'Brandon Draws'
    language = 'en'
    url = 'http://drawbrandondraw.com/'
    start_date = '2010-06-29'
    rights = 'by Brandon D, Creative Commons Share-Alike 3.0'

class ComicTextParser(HTMLParser):
    visible_text = None

    def handle_data(self, text):
        if self.visible_text is None:
            self.visible_text = text
        else:
            self.visible_text += text

class Crawler(CrawlerBase):
    history_capable_date = '2010-06-29'
    time_zone = -8

    def crawl(self, pub_date):
        page_url = 'http://drawbrandondraw.com/index.php?date=%s' % \
            pub_date.strftime('%Y-%m-%d')
        page = self.parse_page(page_url)

        url = page.src('div[id="content"] img')

        # There's a lot of malformed HTML from Project Wonderful in the text.
        # There's some CSS tags sometimes, too: I'll just leave those in as
        # parsing them out requires a CSS parser and Python Proper doesn't
        # have one integrated.
        text = re.sub(r'\s{2,}', '\n\n', page.text('div#news')).strip()

        text_parser = ComicTextParser()
        text_parser.feed(text)
        text_parser.close()
        text = text_parser.visible_text

        return CrawlerImage(url, text=text)
