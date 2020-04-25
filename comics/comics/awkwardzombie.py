from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Awkward Zombie"
    language = "en"
    url = "http://www.awkwardzombie.com/"
    start_date = "2006-09-20"
    rights = "Katie Tiedrich"


class Crawler(CrawlerBase):
    history_capable_date = "2006-09-20"
    schedule = "Mo"
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        page = self.parse_page(
            pub_date.strftime("http://www.awkwardzombie.com/?comic=%m%d%y")
        )

        page_date = page.text("#date").strip()
        page_date = page_date.replace("st,", ",")
        page_date = page_date.replace("nd,", ",")
        page_date = page_date.replace("rd,", ",")
        page_date = page_date.replace("th,", ",")
        try:
            page_date = self.string_to_date(page_date, "%B %d, %Y")
        except ValueError:
            return
        if page_date != pub_date:
            return

        result = [
            CrawlerImage(url)
            for url in page.src("#comic img", allow_multiple=True)
        ]
        if result:
            result[0].title = page.text(".title").strip()
        return result
