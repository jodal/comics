from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Devil Bear"
    language = "en"
    url = "http://www.thedevilbear.com/"
    start_date = "2009-01-01"
    rights = "Ben Bourbon"


class Crawler(CrawlerBase):
    history_capable_days = 0
    schedule = "Tu,We,Th,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        page = self.parse_page("http://www.thedevilbear.com/")
        url = page.src("#comic img")
        return CrawlerImage(url)
