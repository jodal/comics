from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Calvin and Hobbes"
    language = "en"
    url = "https://www.gocomics.com/calvinandhobbes"
    start_date = "1985-11-18"
    end_date = "1995-12-31"
    rights = "Bill Watterson"


class Crawler(GoComicsCrawlerBase):
    url_name = "calvinandhobbes"
    history_start_date = "1985-11-18"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"
