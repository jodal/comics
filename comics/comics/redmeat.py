from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Red Meat"
    language = "en"
    url = "http://www.redmeat.com/"
    start_date = "1996-06-10"
    rights = "Max Cannon"


class Crawler(CrawlerBase):
    schedule = "Tu"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        page = self.parse_page("http://www.redmeat.com/max-cannon/FreshMeat")
        url = page.src(".comicStrip img")
        title = page.alt(".comicStrip img")
        if pub_date.strftime("%Y-%m-%d") not in url:
            return
        return CrawlerImage(url, title)
