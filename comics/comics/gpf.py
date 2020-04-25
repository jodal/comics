from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "General Protection Fault"
    language = "en"
    url = "http://www.gpf-comics.com/"
    start_date = "1998-11-02"
    rights = "Jeffrey T. Darlington"


class Crawler(CrawlerBase):
    history_capable_date = "1998-11-02"
    schedule = "Mo,We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        page_url = "http://www.gpf-comics.com/archive.php?d=%s" % (
            pub_date.strftime("%Y%m%d"),
        )
        page = self.parse_page(page_url)
        url = page.src('img[alt^="[Comic for"]')
        return CrawlerImage(url)
