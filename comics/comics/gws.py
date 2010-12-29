from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Girls With Slingshots'
    language = 'en'
    url = 'http://www.girlswithslingshots.com/'
    start_date = '2004-09-30'
    rights = 'Danielle Corsetto'

class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        page = self.parse_page('http://www.girlswithslingshots.com/')
        url = page.src('div#comic img')
        title = page.title('div#comic img')

        try:
            all_post_ids = page.id('div#blog div.post', allow_multiple=True)
            blog_post_id = all_post_ids[0]
            blog_paragraphs = page.text(
                'div#%s div.entry p' % blog_post_id, allow_multiple=True)
            text = '\n\n'.join(blog_paragraphs)
        except StandardError, e:
            text = None

        return CrawlerImage(url, title, text)
