from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.feed_url = 'http://www.megatokyo.com/rss/megatokyo.xml'
        self.parse_feed()

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry['updated_parsed']) == self.pub_date
                and entry.title.startswith('Comic ')):
                self.title = entry.title.split('"')[1]
                self.web_url = entry.link
                break

        if self.web_url is None:
            return

        self.parse_web_page()

        for image in self.web_page.imgs:
            if 'src' in image and image['src'].startswith('strips/'):
                self.web_url = 'http://www.megatokyo.com/'
                self.url = self.join_web_url(image['src'])
                return
