from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dark Legacy"
    language = "en"
    url = "http://www.darklegacycomics.com/"
    start_date = "2006-01-01"
    rights = "Arad Kedar"


class Crawler(CrawlerBase):
    history_capable_days = 29 * 7  # 7 weekly releases
    schedule = "Su"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.darklegacycomics.com/feed.xml")
        for entry in feed.for_date(pub_date):
            title = entry.title
            page = self.parse_page(entry.link)
            url = page.src("img.comic-image")
            return CrawlerImage(url, title)
