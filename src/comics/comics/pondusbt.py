from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.pondus import ComicData as PondusData


class ComicData(PondusData):
    name = "Pondus (bt.no)"
    url = "https://www.bt.no/kultur/tegneserier/"
    active = True


class Crawler(CrawlerBase):
    history_capable_date = "2008-07-01"
    schedule = "Th,Fr,Sa,Su"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        url = "https://cartoon-prod.schibsted.tech/pondus/{}.gif".format(
            pub_date.strftime("%d%m%y"),
        )
        return CrawlerImage(url)
