from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Something Positive"
    language = "en"
    url = "https://somethingpositive.net/"
    start_date = "2001-12-19"
    rights = "R. K. Milholland"


class Crawler(CrawlerBase):
    history_capable_date = "2001-12-19"
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/Chicago"

    def crawl(self, pub_date):
        url = "https://somethingpositive.net/sp{}.png".format(
            pub_date.strftime("%m%d%Y"),
        )
        return CrawlerImage(url)
