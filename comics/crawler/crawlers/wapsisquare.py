import re

from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://wapsisquare.com/d/%(date)s.html' % {
            'date': self.pub_date.strftime('%Y%m%d'),
        }
        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image
                and (image['src'].startswith('/comics/')
                    or ('alt' in image and image['alt'] == "Today's Comic"))):
                m = re.match('.*/\d+_(\w+)\..*', image['src'])
                if m:
                    self.title = m.groups()[0]
                self.url = self.join_web_url(image['src'])
                return
