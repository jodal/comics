from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

import re


class ComicData(ComicDataBase):
    name = 'Subnormality'
    language = 'en'
    url = 'http://www.viruscomix.com/subnormality.html'
    start_date = '2007-01-01'
    rights = 'Winston Rowntree'


class Crawler(CrawlerBase):
    history_capable_date = '2008-11-25'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.viruscomix.com/rss.xml')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            els = filter(lambda el: el.attrib['src'].endswith('.jpg'),
                    page.root.find('body').findall('img'))
            els.sort(key=lambda el: int(
                re.match(r'.*top:\s*(\d+).*', el.attrib['style']).group(1)))
            result = [CrawlerImage(el.attrib['src'], None, el.attrib.get('title', None))
                    for el in els]
            if result:
                result[0].title = page.text('title')
            return result
