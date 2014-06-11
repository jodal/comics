from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Crooked Gremlins'
    language = 'en'
    url = 'http://www.crookedgremlins.com/'
    start_date = '2008-04-01'
    rights = 'Carter Fort and Paul Lucci'


class Crawler(CrawlerBase):
    history_capable_date = '2008-04-01'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        page = self.parse_page(
            'http://crookedgremlins.com/%s/' % pub_date.strftime('%Y/%m/%d'))
        title = page.alt('#comic img')
        url = page.src('#comic img')

        # Put together the text from multiple paragraphs
        text_paragraphs = page.text('.post-content p', allow_multiple=True)
        if text_paragraphs is not None:
            text = '\n\n'.join(text_paragraphs)
        else:
            text = None

        return CrawlerImage(url, title, text)
