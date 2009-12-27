import re

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "KAL's Cartoon"
    language = 'en'
    url = 'http://www.economist.com'
    start_date = '2006-01-05'
    rights = 'Kevin Kallaugher'

class Crawler(CrawlerBase):
    history_capable_days = 1000
    schedule = 'Th'

    def crawl(self, pub_date):
        article_list = self.parse_page('http://www.economist.com/research/articlesBySubject/display.cfm?id=8717275&startRow=1&endrow=500')
        article_list.remove('.web-only')

        for block in article_list.root.cssselect('.article-list .block'):
            date = block.cssselect('.date')[0].text_content()
            regexp = pub_date.strftime('%b %d(st|nd|rd|th) %Y')

            if not re.match(regexp, date):
                continue

            anchor = block.cssselect('h2 a')[0]

            if "KAL's cartoon" not in anchor.text_content():
                continue

            page = self.parse_page(anchor.get('href'))
            return CrawlerResult(page.src('.content-image-full img'))
