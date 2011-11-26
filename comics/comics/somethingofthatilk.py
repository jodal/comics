from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Something of that ilk'
    language = 'en'
    url = 'http://www.somethingofthatilk.com/'
    start_date = '2011-02-19'
    rights = 'Ty Devries'

class Crawler(CrawlerBase):
    history_capable_days = 1
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        page = self.parse_page('http://www.somethingofthatilk.com/')
        url = 'http://www.somethingofthatilk.com/'
        url = page.src('img[src*="/comics/"]')
        
        print '\n\n', url, '\n\n'        

        return CrawlerImage(url)
