from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Luann"
    language = "en"
    url = "https://www.gocomics.com/luann"
    rights = "Greg Evans and Karen Evans"


class Crawler(GoComicsCrawlerBase):
    url_name = "luann"
    history_capable_date = "1985-03-17"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
