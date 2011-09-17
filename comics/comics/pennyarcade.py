from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Penny Arcade'
    language = 'en'
    url = 'http://www.penny-arcade.com/'
    start_date = '1998-11-18'
    rights = 'Mike Krahulik & Jerry Holkins'

class Crawler(CrawlerBase):
    history_capable_date = '1998-11-18'
    schedule = 'Mo,We,Fr'

    def crawl(self, pub_date):
        page_url = 'http://www.penny-arcade.com/comic/%s/' % (
            pub_date.strftime('%Y/%m/%d'),)
        page = self.parse_page(page_url)
        title = page.text('#pageTitle h2')
        url = page.src('.comic img')
        return CrawlerImage(url, title)
