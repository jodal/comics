from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Sherman's Lagoon"
    language = "en"
    url = "https://shermanslagoon.com"
    start_date = "1991-05-13"
    rights = "Jim Toomey"


class Crawler(GoComicsCrawlerBase):
    url_name = "shermanslagoon"
    history_start_date = "2003-12-29"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
