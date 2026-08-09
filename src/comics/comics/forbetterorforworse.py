from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "For Better or For Worse"
    language = "en"
    url = "https://www.gocomics.com/forbetterorforworse"
    start_date = "1981-11-23"
    rights = "Lynn Johnston"


class Crawler(GoComicsCrawlerBase):
    url_name = "forbetterorforworse"
    history_capable_date = "1981-11-23"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
