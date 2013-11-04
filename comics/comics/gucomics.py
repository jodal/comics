from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'GU Comics'
    language = 'en'
    url = 'http://www.gucomics.com/'
    start_date = '2000-07-10'
    rights = 'Woody Hearn'


class Crawler(CrawlerBase):
    history_capable_date = '2000-07-10'
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        page_url = 'http://www.gucomics.com/' + pub_date.strftime('%Y%m%d')
        page = self.parse_page(page_url)

        title = page.text('b')
        title = title.replace('"', '')
        title = title.strip()

        text = page.text('font[class="main"]')
        #  If there is a --- the text after is not about the comic
        text = text[:text.find('---')]
        text = text.strip()

        url = 'http://www.gucomics.com/comics/' + pub_date.strftime('%Y/gu_%Y%m%d')+'.jpg'

        return CrawlerImage(url, title, text)
