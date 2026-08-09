from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "F Minus"
    language = "en"
    url = "https://www.gocomics.com/fminus"
    start_date = "1999-09-01"
    rights = "Tony Carrillo"


class Crawler(GoComicsCrawlerBase):
    url_name = "fminus"
    history_capable_date = "2005-05-10"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"
