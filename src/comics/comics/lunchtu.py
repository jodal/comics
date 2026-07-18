from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lunch (tu.no)"
    language = "no"
    url = "https://www.tu.no/lunch/"
    start_date = "2009-10-21"
    rights = "Børge Lund"


class Crawler(CrawlerBase):
    history_capable_days = 20
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "Europe/Oslo"

    # Without referer, the server returns a placeholder image
    headers = {"Referer": "https://www.tu.no/lunch/"}

    def crawl(self, pub_date):
        url = (
            f"https://www.tu.no/api/widgets/comics?name=lunch&date={pub_date:%Y-%m-%d}"
        )
        return CrawlerImage(url)
