from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Crooked Gremlins'
    language = 'en'
    url = 'http://www.crookedgremlins.com/'
    start_date = '2008-04-01'
    rights = 'Carter Fort and Paul Lucci'

class Crawler(CrawlerBase):
    history_capable_date = '2008-04-01'
    time_zone = -8

    def crawl(self, pub_date):
        page_url = Meta.url + pub_date.strftime(r'%m/%d/%Y/')
        page = self.parse_page(page_url)

        image_location = 'div#content > img'
        title = page.title(image_location)
        url = page.src(image_location)

        # Put together the text from multiple paragraphs
        text_paragraphs = page.text('div.entry p', allow_multiple=True)
        if text_paragraphs is not None:
            text = '\n\n'.join(text_paragraphs)
        else:
            text = None

        return CrawlerImage(url, title, text)
