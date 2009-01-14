import re

from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.aftenposten.no/tegneserier/'
        self.parse_web_page()

        strip_pattern = re.compile(
            r'.*/_[Ww]t_\w+_(\d{6})_\w{3}_\d{6}z.jpg$')
        for image in self.web_page.imgs:
            if 'src' in image:
                matches = strip_pattern.match(image['src'])
                if matches is not None:
                    pub_date_string = matches.groups()[0]
                    pub_date = self.string_to_date(pub_date_string, '%y%m%d')
                    if pub_date == self.pub_date:
                        self.url = self.join_web_url(image['src'])
                        self.url = self.url.replace('z.jpg', 'x.jpg')
                        return
