from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Tank McNamara"
    language = "en"
    url = "https://www.gocomics.com/tankmcnamara"
    start_date = "1998-01-01"
    rights = "Wiley Miller"


class Crawler(GoComicsCrawlerBase):
    url_name = "tankmcnamara"
    history_start_date = "1998-01-01"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"
