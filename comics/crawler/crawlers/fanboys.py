from comics.crawler.crawlers import BaseComicCrawler

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://fanboys-online.com/rss/comic.xml')

        for entry in self.feed['entries']:
            if (self.timestamp_to_date(entry['updated_parsed']) == self.pub_date
                and entry['title'].startswith('Comic:')):
                self.title = entry['title'].replace('Comic: ', '')
                self.url = 'http://fanboys-online.com/comics/%(date)s.jpg' % {
                    'date': self.pub_date.strftime('%Y%m%d'),
                }
                return
