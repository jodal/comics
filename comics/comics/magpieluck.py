from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Magpie Luck'
    language = 'en'
    url = 'http://magpieluck.com/'
    start_date = '2009-07-30'
    rights = 'Katie Sekelsky, CC BY-NC-SA 3.0'

class Crawler(CrawlerBase):
    history_capable_days = 0
    schedule = 'Tu,Th'
    time_zone = -5

    def crawl(self, pub_date):
        page = self.parse_page('http://magpieluck.com/')

        # Make sure the date in the corner matches the date for the comic
        test_date = page.text('div#date p')
        if test_date != pub_date.strftime('%B %d, %Y').replace(' 0', ' '):
            return

        url = page.src('div.comic img[title]')
        text = page.alt('div.comic img[title]')
        return CrawlerImage(url, text=text)
