from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Non Sequitur"
    language = "en"
    url = "https://www.gocomics.com/nonsequitur"
    start_date = "1992-02-16"
    rights = "Wiley Miller"


class Crawler(GoComicsCrawlerBase):
    url_name = "nonsequitur"
    history_start_date = "1992-02-16"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
