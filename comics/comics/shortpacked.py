from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Shortpacked'
    language = 'en'
    url = 'http://www.shortpacked.com/'
    start_date = '2005-01-17'
    rights = 'David Willis'

class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8

    def crawl(self, pub_date):
        page = self.parse_page('http://www.shortpacked.com/')
        url = page.src('div.comicpane img')
        title = page.title('div.comicpane img')

        try:
            all_post_classes = page._get('class', 'div[class*="post"]',
                allow_multiple=True)
            post_id = all_post_classes[0].split(' ')[0]
            all_paragraphs = page.text('div[class*="%s"] p' % post_id,
                allow_multiple=True)
            text = '\n\n'.join(all_paragraphs)
        except StandardError:
            text = None

        return CrawlerImage(url, title, text)
