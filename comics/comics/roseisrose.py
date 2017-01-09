from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Rose Is Rose'
    language = 'en'
    url = 'http://www.gocomics.com/roseisrose/'
    start_date = '1984-10-02'
    rights = 'Pat Brady'


class Crawler(CrawlerBase):
    history_capable_date = '1995-10-09'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        headers = {'Referer': 'http://www.gocomics.com/roseisrose'}
        pageurl = 'http://www.gocomics.com/roseisrose/%s' % (pub_date.strftime('%Y/%m/%d'),)
        page = self.parse_page(pageurl)
        url = page.src('img[alt="Rose is Rose"]')
        print url
        return CrawlerImage(url)
