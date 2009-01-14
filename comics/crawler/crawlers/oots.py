from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.feed_url = 'http://www.giantitp.com/comics/oots.rss'
        self.parse_feed()

        if len(self.feed.entries):
            entry = self.feed.entries[0]
            if 'title' in entry:
                self.title = entry.title
            if 'link' in entry:
                self.web_url = entry.link

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if 'src' in image and image['src'].startswith('/comics/images/'):
                self.url = self.join_web_url(image['src'])
                return
