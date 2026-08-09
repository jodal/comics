from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Betty"
    language = "en"
    url = "https://www.gocomics.com/betty"
    start_date = "1991-01-01"
    rights = "Delainey & Gerry Rasmussen"


class Crawler(GoComicsCrawlerBase):
    url_name = "betty"
    history_capable_date = "2008-10-13"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
