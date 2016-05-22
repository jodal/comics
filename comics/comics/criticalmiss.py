from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Critical miss'
    language = 'en'
    url = 'http://www.escapistmagazine.com/articles/view/comicsandcosplay/comics/critical-miss'
    start_date = '2010-05-18'
    rights = 'Cory Rydell & Grey Carter'


class Crawler(CrawlerBase):
    history_capable_days = 200
    schedule = 'Tu,Fr'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://rss.escapistmagazine.com/articles/comicsandcosplay/comics/critical-miss')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('.body img[src$=".png"]')
            title = entry.title
            if title is not None:
                title = title.replace('Critical Miss: ', '')
            return CrawlerImage(url, title)
