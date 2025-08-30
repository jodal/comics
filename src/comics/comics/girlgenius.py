from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Girl Genius"
    language = "en"
    url = "https://www.girlgeniusonline.com/"
    start_date = "2002-11-04"
    rights = "Studio Foglio, LLC"


class Crawler(CrawlerBase):
    history_capable_date = "2002-11-04"
    schedule = "Mo,We,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        url = "https://www.girlgeniusonline.com/ggmain/strips/ggmain{}b.jpg".format(
            pub_date.strftime("%Y%m%d"),
        )
        return CrawlerImage(url)
