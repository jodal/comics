from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.countyoursheep.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        self.parse_web_page()

        for image in self.web_page.imgs:
            if 'src' in image and image['src'].startswith('/comics/'):
                self.url = self.join_web_url(image['src'])
                return
