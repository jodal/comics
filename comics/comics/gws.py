from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Girls With Slingshots"
    language = "en"
    url = "http://www.girlswithslingshots.com/"
    start_date = "2004-09-30"
    rights = "Danielle Corsetto"


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.girlswithslingshots.com/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src("img#cc-comic")
            title = entry.title.replace("Girls with Slingshots - ", "")
            text = page.title("img#cc-comic")
            return CrawlerImage(url, title, text)
