from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nemi (bt.no)"
    language = "no"
    url = "https://www.bt.no/kultur/tegneserier/"
    start_date = "1997-01-01"
    rights = "Lise Myhre"


class Crawler(CrawlerBase):
    history_capable_date = "2008-07-01"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        url = "https://cartoon-prod.schibsted.tech/nemi/{}.gif".format(
            pub_date.strftime("%d%m%y"),
        )
        return CrawlerImage(url)
