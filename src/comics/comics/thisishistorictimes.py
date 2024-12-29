from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "This is Historic Times"
    language = "en"
    url = "http://www.thisishistorictimes.com/"
    start_date = "2006-01-01"
    rights = "Terrence Nowicki, Jr."


class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://thisishistorictimes.com/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
