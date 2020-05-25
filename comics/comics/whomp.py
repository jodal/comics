from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Whomp!"
    language = "en"
    url = "http://www.whompcomic.com/"
    start_date = "2010-06-14"
    rights = "Ronnie Filyaw"


class Crawler(CrawlerBase):
    history_capable_days = 70
    schedule = "We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.whompcomic.com/comic/rss")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src("img#cc-comic")
            text = page.title("img#cc-comic")
            title = entry.title.replace("Whomp! - ", "")

            return CrawlerImage(url, title, text)
