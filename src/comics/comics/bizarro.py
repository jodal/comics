from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Bizarro"
    language = "en"
    url = "https://www.comicskingdom.com/bizarro"
    start_date = "1985-01-01"
    rights = "Dan Piraro"


class Crawler(ComicsKingdomCrawlerBase):
    url_name = "bizarro"
    history_start_date = "2004-03-09"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
