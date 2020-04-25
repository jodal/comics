from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Awkward Zombie"
    language = "en"
    url = "http://www.awkwardzombie.com/"
    start_date = "2006-09-20"
    rights = "Katie Tiedrich"


class Crawler(CrawlerBase):
    history_capable_days = 8
    schedule = "Mo"
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        page = self.parse_page("https://www.awkwardzombie.com/")

        page_epoch = page.src("#cc-comic")
        page_epoch = page_epoch.rsplit("/", 1)[-1]
        page_epoch = page_epoch.split("-", 1)[0]
        try:
            page_epoch = int(page_epoch)
        except ValueError:
            return

        pub_date_start = self.date_to_epoch(pub_date)
        pub_date_end = pub_date_start + 24 * 60 * 60
        if not (pub_date_start < page_epoch < pub_date_end):
            return

        result = [
            CrawlerImage(url)
            for url in page.src("#cc-comic", allow_multiple=True)
        ]
        if result:
            result[0].title = page.title("#cc-comic").strip()
        return result
