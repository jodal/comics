from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Toothpaste for Dinner'
    language = 'en'
    url = 'http://www.toothpastefordinner.com/'
    start_date = '2004-01-01'
    rights = 'Drew'


class Crawler(CrawlerBase):
    history_capable_days = 21
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    # Without User-Agent set, the server returns 302 Found
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.toothpastefordinner.com/rss/rss.php')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src(
                'img[src*="/%s/"]' % pub_date.strftime('%m%d%y'))
            title = entry.title
            return CrawlerImage(url, title)
