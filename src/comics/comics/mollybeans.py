from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Molly Beans"
    language = "en"
    url = "http://www.mollybeans.com/"
    start_date = "2016-02-11"
    rights = "Dan Sacharow"
    end_date = "2019-06-14"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2019-05-08"
    schedule = "We,Fr"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.mollybeans.com/feed/")
        for entry in feed.for_date(pub_date):
            title = entry.title
            if "/comic/" not in entry.link:
                continue
            page = self.parse_page(entry.link)
            url = page.src("img.attachment-panel-comic-strip")
            return CrawlerImage(url, title)
