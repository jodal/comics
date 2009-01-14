from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.feed_url = 'http://www.whiteninjacomics.com/rss/z-latest.xml'
        self.parse_feed()

        for entry in self.feed['entries']:
            if ('updated_parsed' in entry and
                entry['updated_parsed'] is not None
                and self.timestamp_to_date(entry['updated_parsed'])
                    == self.pub_date):
                self.title = entry['title'].split(' - ')[0]
                self.web_url = entry['link']
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and image['src'].startswith('/images/comics/')
                and not image['src'].startswith('/images/comics/t-')):
                self.url = self.join_web_url(image['src'])
                return
