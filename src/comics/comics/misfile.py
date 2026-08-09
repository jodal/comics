from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Misfile"
    language = "en"
    url = "http://www.misfile.com/"
    start_date = "2004-03-01"
    rights = "Chris Hazelton"


class Crawler(ComicControlCrawlerBase):
    base_url = Metadata.url
    history_capable_days = 10
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"
