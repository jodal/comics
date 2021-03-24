from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Penny Arcade"
    language = "en"
    url = "http://penny-arcade.com/"
    start_date = "1998-11-18"
    rights = "Mike Krahulik & Jerry Holkins"


class Crawler(CrawlerBase):
    history_capable_date = "1998-11-18"
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        page_url = "http://penny-arcade.com/comic/{}".format(
            pub_date.strftime("%Y/%m/%d")
        )
        page = self.parse_page(page_url)
        # The site gives a 404 page without a real 404 code
        page_title = page.text("title")
        if page_title == "Penny Arcade - 404":
            return

        title = page.alt("#comicFrame img")
        url = page.src("#comicFrame img")
        return CrawlerImage(url, title)
