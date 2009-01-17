import re

from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.feed_url = 'http://www.aftenposten.no/eksport/rss-1_0/?seksjon=tegneserier&utvalg=siste'
        self.parse_feed()

        for entry in self.feed.entries:
            if (entry.title == 'Dagens Wulffmorgenthaler' and
               self.timestamp_to_date(entry.updated_parsed) == self.pub_date):
               self.web_url = entry.link
               break

        if self.web_url is None:
            return

        self.parse_web_page()

        strip_pattern = re.compile(
            r'.*/_(Escenic-)*[Ww]t_\w+_\d{2}_\d{6}x.jpg$')
        for image in self.web_page.imgs:
            if 'src' in image:
                matches = strip_pattern.match(image['src'])
                if matches is not None:
                    self.url = self.join_web_url(image['src'])
                    return
