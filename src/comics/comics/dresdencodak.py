from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dresden Codak"
    language = "en"
    url = "https://dresdencodak.com/"
    start_date = "2007-02-08"
    rights = "Aaron Diaz"


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://dresdencodak.com/feed/")
        for entry in feed.for_date(pub_date):
            if "Comics" not in entry.tags:
                continue
            page = self.parse_page(entry.link)
            results = [
                CrawlerImage(url)
                for url in page.srcs("section.entry-content > p > img")
            ]
            if results:
                results[0].title = entry.title
                results[0].text = "\n\n".join(entry.content0.texts("p")).strip()
                return results
