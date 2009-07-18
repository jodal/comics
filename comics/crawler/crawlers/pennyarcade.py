from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Penny Arcade'
    language = 'en'
    url = 'http://www.penny-arcade.com/'
    start_date = '1998-11-18'
    history_capable_date = '1998-11-18'
    schedule = 'Mo,We,Fr'
    rights = 'Mike Krahulik & Jerry Holkins'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.web_url = 'http://www.penny-arcade.com/comic/%(date)s/' % {
            'date': self.pub_date.strftime('%Y/%m/%d'),
        }
        self.parse_web_page()

        for tag in self.web_page.tags:
            if (tag['tag'] == 'div'
                and 'class' in tag and tag['class'] == 'simpleheader'
                and 'data' in tag):
                self.title = tag['data']
                break

        for img in self.web_page.imgs:
            if 'alt' in img and img['alt'] == self.title and 'src' in img:
                self.url = self.join_web_url(img['src'])
                return
