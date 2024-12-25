from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Least I Could Do"
    language = "en"
    url = "https://www.leasticoulddo.com/"
    start_date = "2003-02-10"
    rights = "Ryan Sohmer & Lar deSouza"


class Crawler(CrawlerBase):
    history_capable_date = "2003-02-10"
    schedule = "Mo,Tu,We,Th,Fr,Sa"
    time_zone = "America/Montreal"

    def crawl(self, pub_date):
        url = "https://leasticoulddo.com/comic/%s" % pub_date.strftime("%Y%m%d")
        page = self.parse_page(url)
        image_url = page.src('img[class="comic"]')

        return CrawlerImage(image_url)
