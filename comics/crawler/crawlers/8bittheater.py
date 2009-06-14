from comics.crawler.crawlers import BaseComicCrawler, BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = '8-Bit Theater',
    language = 'en'
    url = 'http://www.nuklearpower.com/'
    start_date = '2001-03-02'
    history_capable_date = '2001-03-02'
    schedule = 'Tu,Th,Sa'
    time_zone = -6
    rights = 'Brian Clevinger'

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
