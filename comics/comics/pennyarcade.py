from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Penny Arcade"
    language = "en"
    url = "https://penny-arcade.com/"
    start_date = "1998-11-18"
    rights = "Mike Krahulik & Jerry Holkins"


class Crawler(CrawlerBase):
    history_capable_date = "1998-11-18"
    schedule = "Mo,We,Fr"
    time_zone = "US/Pacific"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        page_url = "https://penny-arcade.com/comic/{}".format(
            pub_date.strftime("%Y/%m/%d")
        )
        page = self.parse_page(page_url)
        title = page.content('meta[property="og:title"]').replace(" - Penny Arcade", "")
        url = page.content('meta[property="og:image"]')
        # The site gives a 404 page without a real 404 code
        if title == "Not Found (#404)":
            return
        return CrawlerImage(url, title)
