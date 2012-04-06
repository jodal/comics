from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Atheist Cartoons'
    language = 'en'
    url = 'http://www.atheistcartoons.com/'
    start_date = '2009-01-03'
    rights = 'Atheist Cartoons'

class Crawler(CrawlerBase):
    history_capable_date = '2009-01-03'
    schedule = None
    time_zone = 9

    def crawl(self, pub_date):
        page_url = 'http://www.atheistcartoons.com/?m=%s' % \
            pub_date.strftime('%Y%m%d')
        page = self.parse_page(page_url)

        url = page.src('div[class="entry"] img')
        title = page.text('div[class="entry"] > h2 a')

        return CrawlerImage(url, title)
