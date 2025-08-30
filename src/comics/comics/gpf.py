from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "General Protection Fault"
    language = "en"
    url = "https://www.gpf-comics.com/"
    start_date = "1998-11-02"
    rights = "Jeffrey T. Darlington"


class Crawler(CrawlerBase):
    history_capable_date = "1998-11-02"
    schedule = "Mo"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        page_url = "https://www.gpf-comics.com/archive.php?d={}".format(
            pub_date.strftime("%Y%m%d"),
        )
        page = self.parse_page(page_url)
        url = page.src('img[alt^="[Comic for"]')
        return CrawlerImage(url)
