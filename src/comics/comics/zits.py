from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Zits"
    language = "en"
    url = "http://zitscomics.com/"
    start_date = "1997-07-01"
    rights = "Jerry Scott and Jim Borgman"


class Crawler(ComicsKingdomCrawlerBase):
    url_name = "zits"
    history_capable_date = "1997-07-13"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
