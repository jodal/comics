from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "The Boondocks"
    language = "en"
    url = "https://www.gocomics.com/boondocks"
    start_date = "1999-04-19"
    rights = "Aaron McGruder"


class Crawler(GoComicsCrawlerBase):
    url_name = "boondocks"
    history_start_date = "1999-04-19"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"
