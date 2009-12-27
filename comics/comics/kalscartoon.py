from dateutil.parser import parse

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "KAL's Cartoon"
    language = 'en'
    url = 'http://www.economist.com/'
    start_date = '2006-01-05'
    rights = 'Kevin Kallaugher'

class Crawler(CrawlerBase):
    history_capable_date = '2006-01-05'
    schedule = 'Th'

    def crawl(self, pub_date):
        article_list = self.parse_page('http://www.economist.com/'
            'research/articlesBySubject/display.cfm'
            '?id=8717275&startRow=1&endrow=1000')
        article_list.remove('.web-only')
        for block in article_list.root.cssselect('.article-list .block'):
            date = block.cssselect('.date')[0]
            if pub_date != parse(date.text_content()).date():
                continue
            anchor = blockdate.cssselect('h2 a')[0]
            if "KAL's cartoon" not in anchor.text_content():
                continue
            page = self.parse_page(anchor.get('href'))
            url = page.src('.content-image-full img')
            return CrawlerResult(url)
