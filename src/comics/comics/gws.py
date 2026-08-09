from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Girls With Slingshots"
    language = "en"
    url = "http://www.girlswithslingshots.com/"
    start_date = "2004-09-30"
    rights = "Danielle Corsetto"


class Crawler(ComicControlCrawlerBase):
    base_url = Metadata.url
    history_capable_days = 30
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"
