from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Oatmeal"
    language = "en"
    url = "http://theoatmeal.com/"
    rights = "Matthew Inman"


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/oatmealfeed")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            results = [
                CrawlerImage(url)
                for url in page.src('img[src*="/comics/"]', allow_multiple=True)
            ]
            if results:
                results[0].title = entry.title
                return results
