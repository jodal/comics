from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'rhymes with witch'
    language = 'en'
    url = 'http://www.rhymes-with-witch.com/'
    start_date = '2006-08-09'
    rights = 'r*k*milholland'

class Crawler(CrawlerBase):
    schedule = None

    def crawl(self, pub_date):
        page_url = 'http://www.rhymes-with-witch.com/rww%s.shtml' % (
            pub_date.strftime('%m%d%Y'),)
        page = self.parse_page(page_url)
        url = page.src('div > img')
        return CrawlerImage(url)
