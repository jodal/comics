from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.nuklearpower.com/daily.php?date=%s' % (
            self.pub_date.strftime('%y%m%d'),
        )
        self.parse_web_page()

        for image in self.web_page.imgs:
            if ('src' in image and image['src'].startswith(
                'http://www.nuklearpower.com/comics/')):
                self.url = self.join_web_url(image['src'])
                for tag in self.web_page.tags:
                    if 'data' in tag and tag['data'].startswith('Episode'):
                        self.title = tag['data']
                        return
