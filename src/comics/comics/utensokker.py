from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Uten Sokker"
    language = "no"
    url = "https://nettserier.no/utensokker/"
    active = False
    start_date = "2009-07-14"
    end_date = "2018-04-17"
    rights = "Bjørnar Grandalen"


class Crawler(NettserierCrawlerBase):
    history_capable_date = "2009-07-14"
    time_zone = "Europe/Oslo"
