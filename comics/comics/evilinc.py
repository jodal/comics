from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Evil Inc.'
    language = 'en'
    url = 'http://www.evil-comic.com/'
    start_date = '2005-05-30'
    rights = 'Brad J. Guigar - Colorist: Ed Ryzowski'

class Crawler(CrawlerBase):
    history_capable_date = '2005-05-30'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'

    def crawl(self, pub_date):
        page_url = 'http://www.evil-comic.com/archive/%s.html' % (
            pub_date.strftime('%Y%m%d'))

        page = self.parse_page(page_url)

        # Page does not generate 404, redirects to archive page instead
        if page.url() != page_url:
            return

        url = page.src('#ei_strip')
        title = page.text('#seriesselect option[selected]')

        return CrawlerImage(url, title)
