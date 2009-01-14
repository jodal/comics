from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://ars.userfriendly.org/cartoons/?id=%(date)s' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        self.parse_web_page()

        for img in self.web_page.imgs:
            if ('src' in img and 'alt' in img
                and img['alt'].startswith('Strip for')):
                self.url = self.join_web_url(img['src'])
                return
