from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Rose Is Rose"
    language = "en"
    url = "https://www.gocomics.com/roseisrose"
    start_date = "1984-10-02"
    rights = "Pat Brady"


class Crawler(GoComicsCrawlerBase):
    url_name = "roseisrose"
    history_start_date = "1995-10-09"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
