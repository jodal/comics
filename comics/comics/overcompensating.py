from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Overcompensating'
    language = 'en'
    url = 'http://www.overcompensating.com/'
    start_date = '2004-09-29'
    rights = 'Jeff Rowland'

class Crawler(CrawlerBase):
    history_capable_date = '2004-09-29'
    schedule = None
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        img_locator = 'center > img[title]'
        page = self.parse_page(
            'http://www.overcompensating.com/posts/%s.html' %
            pub_date.strftime('%Y%m%d'))
        url = page.src(img_locator)

        # Make sure that the date is in the src of the comic somewhere... they
        # forward pages that aren't found to the current comic
        if pub_date.strftime('%Y%m%d') not in url:
            return

        text = page.title(img_locator).replace('COMIC MISSING: ', '')
        return CrawlerImage(url, text=text)
