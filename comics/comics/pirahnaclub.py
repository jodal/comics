# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pirahna Club'
    language = 'en'
    url = 'http://piranhaclubcomics.com'
    start_date = '2009-10-21'
    rights = 'Bud Grace'


class Crawler(CrawlerBase):
    history_capable_date = '1998-09-06'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'

    # Without referer, the server returns a placeholder image
#    headers = {'Referer': 'http://www.tu.no/tegneserier/lunch/'}

    def crawl(self, pub_date):
        
        pageurl = 'http://piranhaclubcomics.com/comics/%s/' % (pub_date.strftime('%B-%-d-%Y'),)
        print pageurl
        page = self.parse_page(pageurl)
        url = page.src('img[src^="https://safr.kingfeatures.com/idn/cnfeed/zone/js/content.php?file="]')
        return CrawlerImage(url)
