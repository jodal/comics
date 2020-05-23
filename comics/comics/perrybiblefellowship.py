from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Perry Bible Fellowship"
    language = "en"
    url = "http://www.pbfcomics.com/"
    start_date = "2001-01-01"
    rights = "Nicholas Gurewitch"


class Crawler(CrawlerBase):
    history_capable_date = "2019-06-12"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.pbfcomics.com/feed/feed.xml")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            images = page.root.xpath("//div[@id='comic']/img")
            crawler_images = []
            for image in images:
                title = entry.title
                crawler_images.append(CrawlerImage(image.get("src"), title))
