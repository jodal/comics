from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Beetle Bailey"
    language = "en"
    url = "https://www.comicskingdom.com/beetle-bailey-1"
    start_date = "1950-01-01"
    rights = "Mort Walker"


class Crawler(ComicsKingdomCrawlerBase):
    url_name = "beetle-bailey-1"
    history_start_date = "1953-10-05"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
