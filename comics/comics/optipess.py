# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Optipess'
    language = 'en'
    url = 'http://www.optipess.com/'
    start_date = '2008-12-01'
    rights = 'Kristian Nygård'


class Crawler(CrawlerBase):
    history_capable_date = '2008-12-01'
    schedule = 'Mo,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        # Find the post for the requested date
        date_string = pub_date.strftime('%Y/%m/%d')
        date_page = self.parse_page('http://www.optipess.com/%s' % date_string)
        post_link = date_page.root.xpath('//h2[@class="post-title"]/a')[0]
        title = post_link.text
        # Fetch the actual post
        page = self.parse_page(post_link.get('href'))
        url = page.src('img[src*="/comics/"]')
        text = page.title('img[src*="/comics/"]')
        return CrawlerImage(url, title, text)
