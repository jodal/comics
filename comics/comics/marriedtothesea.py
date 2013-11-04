from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Married To The Sea'
    language = 'en'
    url = 'http://www.marriedtothesea.com/'
    start_date = '2006-02-13'
    rights = 'Drew'


class Crawler(CrawlerBase):
    history_capable_date = '2006-02-13'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page_url = 'http://www.marriedtothesea.com/index.php?date=' + pub_date.strftime('%m%d%y')
        page = self.parse_page(page_url)
        url = page.src('#butts img', allow_multiple=True)[0]
        title = page.text('div[class="headertext"]', allow_multiple=True)
        title = title[0]
        title = title[title.find(':')+1:].strip()
        return CrawlerImage(url, title)
