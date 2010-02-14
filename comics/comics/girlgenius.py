from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Girl Genius'
    language = 'en'
    url = 'http://www.girlgeniusonline.com/'
    start_date = '2002-11-04'
    rights = 'Copyright 2000-2010 Studio Foglio, LLC'

class Crawler(CrawlerBase):
    history_capable_date = '2002-11-04'
    schedule = 'Mo,We,Fr'
    time_zone = -8
    has_rerun_releases = False

    def crawl(self, pub_date):
        return CrawlerImage("http://www.girlgeniusonline.com/ggmain/strips/ggmain%sb.jpg" % pub_date.strftime( '%Y%m%d' ))
